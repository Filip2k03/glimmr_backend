from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add any custom fields here if needed, otherwise just use AbstractUser's fields
    # e.g., bio = models.TextField(max_length=500, blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users_custom_set', # Unique related_name for groups
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users_custom_permissions_set', # Unique related_name for user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following') # A user can only follow another user once

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"