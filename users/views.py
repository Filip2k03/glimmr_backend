from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer
from .models import Follow

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class CurrentUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username' # Allows lookup by username

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class FollowUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, username, format=None):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == target_user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)

        if created:
            return Response({'detail': f'You are now following {target_user.username}.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': f'You are already following {target_user.username}.'}, status=status.HTTP_200_OK)

class UnfollowUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, username, format=None):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == target_user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Follow.objects.filter(follower=request.user, following=target_user).delete()

        if deleted_count > 0:
            return Response({'detail': f'You have unfollowed {target_user.username}.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'You were not following {target_user.username}.'}, status=status.HTTP_200_OK)