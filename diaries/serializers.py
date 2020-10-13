from rest_framework import serializers
from .models import Diary, Like  # 같은 앱 내이니까 .models


class DiarySerializer(serializers.ModelSerializer):

    # ADDITIONAL FIELD
    likes = serializers.SerializerMethodField()
    username = serializers.CharField(
        source='user.username', read_only=True)
    admin_name = serializers.CharField(
        source='userLesson.lesson.user.username', read_only=True)

    class Meta:
        model = Diary
        fields = ['id', 'userLesson', 'userLesson_id', 'content',  'mood', 'img_path',
                  'created', 'likes', 'username', 'admin_name']

    def get_likes(self, diary):
        return Like.objects.filter(diary=diary).count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id']
