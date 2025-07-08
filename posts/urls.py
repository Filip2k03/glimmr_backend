from django.urls import path
from .views import PostListCreateView, PostDetailView, LikePostView, CommentListCreateView, CommentDetailView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('<int:post_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:post_pk>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]