from django.urls import re_path

from site_app import consumers

websocket_urlpatterns = [
    re_path(r'ws/bot/', consumers.EchoConsumerAsync.as_asgi()),
]