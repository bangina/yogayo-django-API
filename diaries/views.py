from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Diary, Like
from .serializers import DiarySerializer, LikeSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from .pagination import PostPageNumberPagination

# 모든 다이어리



class DiaryList(generics.ListCreateAPIView):
    serializer_class = DiarySerializer
    queryset = Diary.objects.all().order_by('-created')
    #인증방식 : Token
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination
    parser_class = (FileUploadParser,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):

        file_serializer = DiarySerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save(user=self.request.user)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 내가 쓴 다이어리
class MyDiaryList(generics.ListCreateAPIView):
    serializer_class = DiarySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        # 요청하는 사람 리스트만 보여주기
        user = self.request.user
        return Diary.objects.filter(user=user).order_by(
            '-created')


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


# 좋아요 & un좋아요
class LikeCreate(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        diary = Diary.objects.get(pk=self.kwargs['pk'])
        return Like.objects.filter(user=user, diary=diary)

    def perform_create(self, serializer, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer.save(user=self.request.user,
                        diary=Diary.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("좋아요하신적이 없는데?뭘 삭제하신단건지..")


# 이미지 업로드뷰
class ImgUploadView(APIView):
    parser_class = (FileUploadParser,)
    serializer_class = DiarySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        file_serializer = DiarySerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
