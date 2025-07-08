from rest_framework import serializers
from .models import ChatRoom, Message
from users.serializers import UserSerializer # Re-use UserSerializer

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ('id', 'name', 'participants', 'created_at', 'is_direct_message', 'last_message')

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True) # Display sender info

    class Meta:
        model = Message
        fields = ('id', 'chat_room', 'sender', 'content', 'timestamp')
        read_only_fields = ('sender', 'chat_room')