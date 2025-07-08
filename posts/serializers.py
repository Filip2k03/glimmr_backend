from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserSerializer # Import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Display user info

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'content', 'created_at')
        read_only_fields = ('user', 'post') # User and post will be set by view

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    media_url = serializers.URLField(source='media.url', read_only=True) # To expose media URL

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'media', 'media_url', 'post_type',
                  'created_at', 'updated_at', 'likes_count', 'comments_count', 'is_liked')
        read_only_fields = ('user', 'likes_count', 'comments_count', 'is_liked', 'media_url')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False