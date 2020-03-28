"""
Data retrieving form google api, data storingin mysql, periodic data retrieving.
"""
import os
import math
from datetime import datetime, timezone, timedelta

import mysql.connector
import googleapiclient.discovery
import googleapiclient.errors
import dateutil.parser

from celery import Celery
from celery.task import periodic_task

from connect import insert_data

# Update time conversion, as it can fail if time changes to summer time
# Update how item's are inserted to db check for 2 values or insert if time uploaded is
# Between some interval

hard_channel_id = 'UCF9IOB2TExg3QIBupFtBDxg'

my_db = mysql.connector.connect(
    option_files='../mysql.cnf'
)
my_cursor = my_db.cursor()


def initialize_youtube():
    """ create youtube client """

    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ['Y3_API_KEY']
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    return youtube


def get_channel_video_ids(channel_id):
    """ Retrieves list of video ids on time online case"""

    youtube = initialize_youtube()
    res = youtube.channels().list(id=channel_id,
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    res = youtube.playlistItems().list(playlistId=playlist_id,
                                       part='snippet',
                                       maxResults=50).execute()

    video_ids = []
    for i in range(len(res)):
        published_at = res['items'][i]['snippet']['publishedAt']
        published_at_iso = dateutil.parser.isoparse(published_at)
        date_time_now = datetime.now(timezone.utc)
        video_online_time = date_time_now - published_at_iso
        print("Time hours online", video_online_time.total_seconds() / 3600)
        # how long video is online < 1 less when hour
        # final version 0.95 < x < 1.05 if code runs in 5 mins interval
        if 0.95 < (video_online_time.total_seconds() / 3600) < 2:
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])

    return video_ids


def get_video_data(video_id, channel_id, mycursor):
    """ get video view data as obj """

    youtube = initialize_youtube()
    now = datetime.now()
    mycursor.execute("SELECT video_views FROM video_data WHERE channel_id=" + \
                     "'" + channel_id + "'")
    all_video_views_db = mycursor.fetchall()
    print('All video views', all_video_views_db)
    mycursor.execute("SELECT video_id FROM video_data")
    video_ids_db = mycursor.fetchall()
    print('Video ids', video_ids_db)
    res = youtube.videos().list(id=video_id,
                                part='statistics').execute()
    views = int(res['items'][0]['statistics']['viewCount'])

    if all_video_views_db:
        video_count = len(all_video_views_db)
        views_list = [x[0] for x in all_video_views_db]
        views_median = math.fsum(views_list) / video_count
        perf_diff = views - views_median
    else:
        views_median = views
        perf_diff = 0

    view_stats = {'time': now,
                  'channel_id': channel_id,
                  'video_id': video_id,
                  'video_views': views,
                  'videos_views_median': views_median,
                  'perf_diff': perf_diff}

    return view_stats


def get_video_tags(video_id):
    """ Get list of tags from video """

    youtube = initialize_youtube()
    res = youtube.videos().list(id=video_id,
                                part='snippet').execute()
    # some videos don`t have tags
    try:
        tags = str(res['items'][0]['snippet']['tags'])
    except IndexError:
        tags = ""

    data_obj = {'tags': tags}

    return data_obj


app = Celery('tasks', broker='pyamqp://guest@localhost//')

@periodic_task(run_every=timedelta(seconds=300))
def colect_insert_data():
    """ Combine retrieved data, store data to database """
    video_ids_list = get_channel_video_ids(hard_channel_id)

    for vid_id in video_ids_list:
        data = get_video_data(vid_id, hard_channel_id, my_cursor)
        tags = get_video_tags(vid_id)
        data.update(tags)
        insert_data(data, 'video_data', my_cursor, my_db)
colect_insert_data()
