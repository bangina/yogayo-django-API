from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username', read_only=True)
    img_profile = serializers.FileField(
        source='user.img_profile', read_only=True)

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'username',
            'img_profile',
            'category',
            'title',
            'content',
            'img_path1',
            'img_path2',
            'img_path3',
            'img_path4',
            'created',
            'views',
            'comments',
        ]

    def get_comments(self, post):
        return Comment.objects.filter(post=post).count()


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username', read_only=True)
    img_profile = serializers.CharField(
        source='user.img_profile', read_only=True)

    class Meta:
        model = Comment
        fields = ['post', 'username', 'content', 'created', 'img_profile']
