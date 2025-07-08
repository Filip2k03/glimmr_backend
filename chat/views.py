from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

User = get_user_model()

class ChatRoomListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # List all chat rooms the current user is a participant in
        return ChatRoom.objects.filter(participants=self.request.user).distinct()

    def create(self, request, *args, **kwargs):
        # This view primarily for creating new group chats or initiating a DM if not exists
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response({"detail": "Participants are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Always include the current user in participants
        participant_ids.append(request.user.id)
        participant_ids = list(set(participant_ids)) # Remove duplicates

        if len(participant_ids) < 2:
            return Response({"detail": "A chat room needs at least two participants."}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response({"detail": "One or more participants not found."}, status=status.HTTP_400_BAD_REQUEST)

        is_dm = (len(participant_ids) == 2)
        room_name = request.data.get('name') if not is_dm else None

        if is_dm:
            # Check if a DM room already exists
            user1 = participants.first()
            user2 = participants.last() # Assuming there are exactly two
            room = ChatRoom.get_or_create_direct_message_room(user1, user2)
            serializer = self.get_serializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK) # Return 200 if already exists

        # For group chats, create a new one
        chat_room = ChatRoom.objects.create(name=room_name, is_direct_message=False)
        chat_room.participants.set(participants) # Set all participants
        serializer = self.get_serializer(chat_room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageListCreateView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_pk = self.kwargs['room_pk']
        # Ensure user is a participant of the chat room
        chat_room = generics.get_object_or_404(ChatRoom, pk=room_pk, participants=self.request.user)
        return chat_room.messages.all()

    # Note: Message creation will primarily happen via WebSocket in consumers.py
    # This view is mainly for fetching history.