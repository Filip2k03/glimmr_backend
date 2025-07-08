import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from .serializers import MessageSerializer # Use your existing serializer

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user'] # User is available thanks to AuthMiddlewareStack

        if not self.user.is_authenticated:
            await self.close(code=4001) # Unauthorized
            return

        # Fetch the chat room
        self.chat_room = await self.get_chat_room(self.room_name)
        if not self.chat_room:
            await self.close(code=4004) # Room not found
            return

        # Check if user is a participant of the room
        is_participant = await database_sync_to_async(self.chat_room.participants.filter)(id=self.user.id)
        if not await database_sync_to_async(is_participant.exists)():
            await self.close(code=4003) # Forbidden
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connected for user {self.user.username} to room {self.room_name}")


    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message')

        if not message_content:
            return

        # Save message to database
        message = await self.create_message(self.user, self.chat_room, message_content)

        # Serialize the message for sending over WebSocket
        serialized_message = await database_sync_to_async(lambda: MessageSerializer(message).data)()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': serialized_message,
                'sender_id': self.user.id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))

    @database_sync_to_async
    def get_chat_room(self, room_name):
        try:
            # Assuming room_name passed here is the 'id' of the ChatRoom
            return ChatRoom.objects.get(id=int(room_name))
        except (ChatRoom.DoesNotExist, ValueError):
            return None

    @database_sync_to_async
    def create_message(self, sender, chat_room, content):
        return Message.objects.create(sender=sender, chat_room=chat_room, content=content)