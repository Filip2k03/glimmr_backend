from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings # For media paths

User = get_user_model()

class Post(models.Model):
    POST_TYPES = (
        ('post', 'Standard Post'),
        ('reel', 'Reel (Short Video)'),
        ('myday', 'MyDay (Story - Ephemeral)'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to='post_media/', blank=True, null=True) # For images or videos
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def media_url(self):
        if self.media:
            return settings.MEDIA_URL + str(self.media)
        return None

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"