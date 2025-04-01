from django.urls import path, re_path
from . import cunsumers

websocket_urlpatterns = [
    re_path(r'ws/schedule/$', cunsumers.ScheduleConsumer.as_asgi()),
]