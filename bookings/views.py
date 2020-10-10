from django.shortcuts import render
from rest_framework import generics
from .models import Lesson, UserLesson
from .serializers import LessonSerializer, UserLessonSerializer


# 날짜별 수업 목록
class LessonList(generics.ListAPIView):

    serializer_class = LessonSerializer

# url로 넘긴 query(date)를 기준으로 filter

    def get_queryset(self):
        queryset = Lesson.objects.all()
        date = Lesson.objects.filter(
            date=self.kwargs.get("date"))
        return date


# My Lesson List(유저 본인이 신청한 수업들 목록)\
class MyLessonList(generics.ListAPIView):
    serializer_class = UserLessonSerializer

    def get_queryset(self):
        queryset = UserLesson.objects.all()
        user = self.request.user
        return UserLesson.objects.filter(user=user)


# 수업별 신청 회원리스트 뷰
class LessonUsersList(generics.ListAPIView):
    serializer_class = UserLessonSerializer

    def get_queryset(self):
        queryset = UserLesson.objects.all()
        lesson = UserLesson.objects.filter(
            lesson=self.kwargs.get("lesson"))
        return lesson
