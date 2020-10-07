from rest_framework import serializers
from .models import Lesson, UserLesson
from django.contrib.auth.models import User


class LessonSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username', read_only=True)

    class Meta:
        model = Lesson
        fields = ['username', 'name', 'room', 'date', 'time', 'max_ppl']


class UserLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLesson
        fields = '__all__'
