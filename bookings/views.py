from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Lesson, UserLesson, VoucherUser, Voucher
from .serializers import LessonSerializer, UserLessonSerializer, BookingSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponse
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
class MyLessonList(generics.ListCreateAPIView):
    serializer_class = UserLessonSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = UserLesson.objects.all()
        user = self.request.user
        return UserLesson.objects.filter(user=user)

    def perform_create(self, serializer):
        lesson = self.request.data.get("lesson")
        user = self.request.data.get("user")
        userLesson = UserLesson.objects.filter(
            user=user, lesson=lesson).all()
        if userLesson.exists():
            print(userLesson)
            return HttpResponse("이미 있는데")
            # return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            print("없음")
        #     serializer.save(user=self.request.user)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# 수업별 신청 회원리스트 뷰
class LessonUsersList(generics.ListAPIView):
    serializer_class = UserLessonSerializer

    def get_queryset(self):
        queryset = UserLesson.objects.all()
        lesson = UserLesson.objects.filter(
            lesson=self.kwargs.get("lesson"))
        return lesson


# 사용자 보유한 회원권 뷰
class UserVoucherList(generics.ListAPIView):
    serializer_class = BookingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = VoucherUser.objects.all()
        user = self.request.user
        return VoucherUser.objects.filter(user=user)

# 이용권 정보
