from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Diary, Like
from .serializers import DiarySerializer, LikeSerializer


class DiaryList(generics.ListCreateAPIView):

    queryset = Diary.objects.all()
    serializer_class = DiarySerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DiaryRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 작성자만 삭제가능

    # 삭제하는 함수
    def delete(self, request, *args, **kwargs):
        diary = Diary.objects.filter(
            pk=self.kwargs['pk'], user=self.request.user)
        if diary.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("그쪽 게시물이 아닌데용!!! 못 지우세요!!")


# 투표하기 & un투표하기
class LikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        diary = Diary.objects.get(pk=self.kwargs['pk'])
        return Like.objects.filter(user=user, diary=diary)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("이미 좋아요하셨어요! :)")
        serializer.save(user=self.request.user,
                        diary=Diary.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("좋아요하신적이 없는데?뭘 삭제하신단건지..")
