from rest_framework import serializers

from .models import VideoData


class VideosDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoData
        fields = '__all__'

