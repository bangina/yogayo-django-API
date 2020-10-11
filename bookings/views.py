from django.shortcuts import render
from rest_framework import generics, permissions, status, mixins
from .models import Lesson, UserLesson, VoucherUser, Voucher
from .serializers import LessonSerializer, UserLessonSerializer, BookingSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
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

# 수강신청 & 취소 처리


class UserLessonCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = UserLessonSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        lesson = Lesson.objects.get(pk=self.kwargs['pk'])
        return UserLesson.objects.filter(user=user, lesson=lesson)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("이미 수강신청하셨어요. :)")
        serializer.save(user=self.request.user,
                        lesson=Lesson.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("이 수업을 수강신청하신 적이 없어요.", code=None)


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
