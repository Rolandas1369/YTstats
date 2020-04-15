# YTstats
This project uses Youtube Data api, mysql for data storage, django, django rest framework, django filtering.

<pre>
Task is divided into teo parts: 
1. Data gathering part from google api, and is located in retrieve_data.
2. Django part yt_stats

Idea of two parts is simple. One will retrieve data, another will display data. If one will crash another will work.

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
cd retrieve_data
and start a task what run each 5 minutes
celery worker -l info -A yt_data --beat
or 

python yt_data to run code once

django part 
cd ../yt_stats
$ python manage.py makemigrations && python manage.py migrate $$ python manage.py runserver
</pre>

