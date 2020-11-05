from django.shortcuts import render
from rest_framework import generics, permissions, status, mixins
from .models import Lesson, UserLesson, VoucherUser, Voucher
from diaries.models import Diary
from .serializers import LessonSerializer, UserLessonSerializer, BookingSerializer, DiaryLessonSerializer, VoucherSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db.models import F
from datetime import datetime, timedelta
from random import *
# 날짜별 수업 목록


class LessonList(generics.ListAPIView):

    serializer_class = LessonSerializer

# url로 넘긴 query(date)를 기준으로 filter

    def get_queryset(self):
        queryset = Lesson.objects.all()
        date = Lesson.objects.filter(
            date=self.kwargs.get("date"))
        return date

# 수업 생성


class AdminLessonList(generics.ListCreateAPIView):

    serializer_class = LessonSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# My Lesson List(유저 본인이 신청한 수업들 목록)\
class MyLessonList(generics.ListCreateAPIView):
    serializer_class = UserLessonSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = UserLesson.objects.all()
        user = self.request.user
        return UserLesson.objects.filter(user=user)

# 수강신청 & 취소 처리 View


class UserLessonCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = UserLessonSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        lesson = Lesson.objects.get(pk=self.kwargs['pk'])
        return UserLesson.objects.filter(user=user, lesson=lesson)
# 수강신청 레코드 생성(&회원 수강권 1회 차감 처리)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("이미 수강신청하셨어요. :)")
        serializer.save(user=self.request.user,
                        lesson=Lesson.objects.get(pk=self.kwargs['pk']))
        voucherUser = VoucherUser.objects.filter(
            user=self.request.user, status=True)
        voucherUser.update(used=F('used') + 1)
        # 수강권 모두 소진시 상태 false로 변경
        # voucher = Voucher.objects.filter(voucher_id=voucherUser.voucher)
        # if voucherUser.used == voucher.limit:
        #     voucherUser.update(status=False)
# 수강신청 레코드 삭제(&회원 수강권 1회 차감 처리)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            voucher = VoucherUser.objects.filter(
                user=self.request.user, status=True)
            voucher.update(used=F('used') - 1)
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
        user = self.request.user
        return VoucherUser.objects.filter(user=user)


class UserVoucherCreate(generics.CreateAPIView):
    serializer_class = BookingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return VoucherUser.objects.filter(user=user)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("이미 수강신청하셨어요. :)")
        serializer.save(user=self.request.user,
                        voucher=Voucher.objects.get(voucherCode=self.kwargs['code']))


# 이용권 정보

# 다이어리 작성 가능한 수업 정보 GET View
class DiaryLessonList(generics.ListAPIView):
    serializer_class = DiaryLessonSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.AllowAny]

#어제와 오늘 참여한 수업만 필터링.
#(수련일기는 어제/오늘 참여한 수업만 작성가능함)
    def get_queryset(self):
        today = datetime.today()
        yesterday = today + timedelta(days=-1)
        user = self.request.user
        userLesson = list(UserLesson.objects.filter(
            date__range=[yesterday, today], user=user))
        obj = []

        for i in userLesson:
            if Diary.objects.filter(userLesson=i).exists():
                obj.append(i)

        for j in obj:
            userLesson.remove(j)

        return userLesson

# 바우쳐 생성


class VoucherList(generics.ListCreateAPIView):
    serializer_class = VoucherSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Voucher.objects.filter(user=user)

    def perform_create(self, serializer):
        voucherCode = 0
        while True:
            code = randint(10000, 99999)
            if Voucher.objects.filter(voucherCode=code).exists():
                continue
            else:
                voucherCode = code
                break
        serializer.save(user=self.request.user, voucherCode=voucherCode)
