# Task
<pre>
Hey!
You need to create a simple application which:
1. Using Youtube API (https://developers.google.com/youtube/v3/) scrapes channel
videos with tags and stats. Also you need to track changes of video stats every N
minutes in order to see how videos are performing. Please pick the interval to scan stats
which, according to you, is efficient and smart. You can hardcode channel ID in code,
that’s not important.
2. Create DB scheme and save scraped data. Please consider, that we will want to scan a
lot of channels, so queries to aggregate and select data shouldn’t take long. Use any database
you feel right.
3. Create mini API, where you can filter videos:
a) By tags.
b) By video performance (first hour views divided by channels all videos first hour
views median)
Bonus points for:
i) pseudo algorithm for fetching as many youtube channels as possible.
ii) unit tests
Requirements:
Python; (use Django/flask framework, please)
MySQL DB;
After finishing task, please send us the bitbucket repository link.
Good Luck :)
</pre>

# YTstats
<pre>
clone project
cd YTstats

create MySQL database 'youtubestats'
create mysql.cnf in root with data
[client]
database = youtubestats
host = localhost
user = DB_USER
password = DB_PASS
default-character-set = utf8

$ virtualenv -p python3 env 
$ source env/bin/activate
$ pip install -r requirements.txt

Project is separated to 2 parts one part data gathering and data insertation:
cd retrive_data
and start a task what run each 5 minutes
celery worker -l info -A yt_data --beat
data is collected if video is beetwean 1 and 2 (final version 0.95 and 1.05) hours online to change this 
edit yt_data.py line 62

django part 
cd ../yt_stats
$ python manage.py makemigrations && python manage.py migrate $$ python manage.py runserver
</pre>

<h1>Pseudo algorithm for as many channel as posible</h1>
<pre>
Sending requests to google api to get new uploaded videos, if new video is uploaded store upload time to db, next, set time to start function if video online time is near 1 hour. If many processes are started at same time, add threads.   
</pre>

