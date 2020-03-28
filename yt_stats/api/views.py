from .serializers import VideosDataSerializer
from rest_framework import generics
from django_filters import rest_framework as filters
from .models import VideoData


class TagFilter(filters.FilterSet):

    class Meta:
        model = VideoData
        fields = {
            'tags': ['contains'],
            'perf_diff': ['range'],
        }


class VideoDataList(generics.ListAPIView):
    queryset = VideoData.objects.all()
    serializer_class = VideosDataSerializer
    filterset_class = TagFilter


    ordering_fields = ['perf_diff']





