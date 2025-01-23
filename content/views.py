from rest_framework import viewsets, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Like, Comment, Share
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, ShareSerializer
from rest_framework.exceptions import AuthenticationFailed
from .utils import get_user_id_from_auth_service





class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  

    
    def perform_create(self, serializer):
        # Fetch the user ID from the auth service
        user_id = get_user_id_from_auth_service(self.request)
        print(f"Fetched User ID: {user_id}")

        # Save the post with the `author_id`
        serializer.save(author_id=user_id)

    def list(self, request, *args, **kwargs):
        # Optional: Filter posts by the authenticated user's ID
        posts = Post.objects.all()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    


class LikePostView(views.APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can like posts

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = Post.objects.get(id=post_id)

        # Check if user has already liked this post
        if Like.objects.filter(post=post, user=request.user).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new like
        like = Like.objects.create(post=post, user=request.user)
        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)
    
    
    

class CommentPostView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = Post.objects.get(id=post_id)

        # Create the comment
        content = request.data.get('content')
        comment = Comment.objects.create(post=post, user=request.user, content=content)

        # Serialize and return the created comment
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SharePostView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = Post.objects.get(id=post_id)

        # Create a share
        share = Share.objects.create(post=post, user=request.user)

        return Response({"detail": "Post shared successfully."}, status=status.HTTP_201_CREATED)