from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, CurrentUserView, UserProfileView, FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Use default JWT login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('profile/<str:username>/follow/', FollowUserView.as_view(), name='follow_user'),
    path('profile/<str:username>/unfollow/', UnfollowUserView.as_view(), name='unfollow_user'),
]