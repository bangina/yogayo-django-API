from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'username',
            'category',
            'title',
            'content',
            'img_path',
            'created',
            'views'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
