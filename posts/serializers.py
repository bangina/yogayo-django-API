from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    # poster = username
    poster = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'content',
            'img_path',
            'created',
            'views',
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
