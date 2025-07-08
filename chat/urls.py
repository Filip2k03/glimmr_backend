from django.urls import path
from .views import ChatRoomListCreateView, MessageListCreateView

urlpatterns = [
    path('', ChatRoomListCreateView.as_view(), name='chat-room-list-create'),
    path('<int:room_pk>/messages/', MessageListCreateView.as_view(), name='message-list'),
]