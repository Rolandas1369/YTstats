from django.urls import path


from .views import VideoDataList

urlpatterns = [
    path('api/', VideoDataList.as_view()),
]