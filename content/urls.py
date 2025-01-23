from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, LikePostView, CommentPostView, SharePostView

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Posts ViewSet (list, create, retrieve)
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/comment/', CommentPostView.as_view(), name='comment-post'),
    path('posts/<int:post_id>/share/', SharePostView.as_view(), name='share-post'),
]