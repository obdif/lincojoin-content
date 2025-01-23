from rest_framework import serializers
from .models import Post, Like, Comment, Share
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    shares_count = serializers.IntegerField(source='shares.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author_id', 'media', 'slug',
            'created_at', 'updated_at', 'likes_count', 'comments_count', 'shares_count',
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


class ShareSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Share
        fields = ['id', 'user', 'post', 'shared_at']