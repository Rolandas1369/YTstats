# Generated by Django 3.0.4 on 2020-03-27 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.CharField(max_length=255)),
                ('tags', models.TextField(blank=True, null=True)),
                ('video_id', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('video_views', models.IntegerField(blank=True, null=True)),
                ('videos_views_median', models.IntegerField(blank=True, null=True)),
                ('perf_diff', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'video_data',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='ChannelVideos',
        ),
        migrations.DeleteModel(
            name='VideoStats',
        ),
        migrations.DeleteModel(
            name='YoutubeChannels',
        ),
    ]
