from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=True, null=True) # For group chats, or auto-generated for DMs
    # For Direct Messages (DMs), ensure only two users. Or just use a direct chat model
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    is_direct_message = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.name:
            return self.name
        else:
            usernames = ", ".join([user.username for user in self.participants.all()])
            return f"DM: {usernames}"

    def get_or_create_direct_message_room(user1, user2):
        # Ensure consistent order for finding existing DM rooms
        participants = sorted([user1.id, user2.id])
        room = ChatRoom.objects.filter(
            is_direct_message=True,
            participants__id=participants[0]
        ).filter(
            participants__id=participants[1]
        ).annotate(
            num_participants=models.Count('participants')
        ).filter(num_participants=2).first()

        if not room:
            room = ChatRoom.objects.create(is_direct_message=True)
            room.participants.add(user1, user2)
        return room


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender.username} in {self.chat_room} at {self.timestamp.strftime('%H:%M')}: {self.content[:50]}..."