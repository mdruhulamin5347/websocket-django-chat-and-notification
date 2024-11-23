from django.urls import re_path
from .consumers import NotificationConsumer,RealTimeChatApp

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/realtimechat/$', RealTimeChatApp.as_asgi()),
]
