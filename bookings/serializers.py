from rest_framework import serializers
from .models import Lesson, UserLesson, VoucherUser, Voucher
from django.contrib.auth.models import User


class LessonSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username', read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'username', 'name', 'room', 'date', 'time', 'max_ppl']


class UserLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLesson
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):

    limit = serializers.IntegerField(source='voucher.limit', read_only=True)
    vouchername = serializers.CharField(source='voucher.name', read_only=True)
    adminname = serializers.CharField(
        source='voucher.user.username', read_only=True)

    class Meta:
        model = VoucherUser
        fields = ['id', 'status', 'str_date',
                  'used', 'user', 'vouchername', 'limit', 'adminname']
