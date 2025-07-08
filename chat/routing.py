from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # WebSocket path for individual chat rooms
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]