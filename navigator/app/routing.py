from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/schedule/$', consumers.ScheduleConsumer.as_asgi()),
]