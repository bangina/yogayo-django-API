from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    # 컬럼 읽기전용으로 만들기
    poster = serializers.ReadOnlyField(source="user.username")
    poster_id = serializers.ReadOnlyField(source="user.id")
    views = serializers.ReadOnlyField(source="views")
    # field에 메소드 추가(votes는 원래 model에 없는 필드)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'poster', 'poster_id', 'category', 'title', 'content', 'img_path',
                  'created', 'views']

    def get_comments(self, post):
        # 함수형태로 해당 post의 코멘트를 가져옴
        return Comment.objects.filter(post=post)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
