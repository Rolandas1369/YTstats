# YTstats

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


<h1>Pseudo algorithm for as many channel as posible</h1>

Sending requests to google api to get new uploaded videos, if new video is uploaded store upload time to db, next, set time to start function if video online time is near 1 hour. If many processes are started at same time, add threads. 



