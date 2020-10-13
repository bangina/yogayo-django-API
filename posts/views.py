from django.shortcuts import render
from rest_framework import generics, permissions

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import F


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by(
        '-created')  # DB에서 쿼리셋 전부 가져왕
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    parser_class = (FileUploadParser,)

    def perform_create(self, serializer):
        # 시리얼라이저야, 저장할 때 poster컬럼은 POST요청자 이름을 넣어
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):

        file_serializer = PostSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save(user=self.request.user)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # 조회수 1 증가 함수
    def get_queryset(self, **kwargs):
        queryset = Post.objects.filter(pk=self.kwargs['pk'])
        queryset.update(views=F('views') + 1)
        print("view 추가")
        return queryset

    # 삭제하는 함수
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(
            pk=self.kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("그쪽 게시물이 아닌데용!!! 못 지우세요!!")


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(post=post).order_by(
            'created')

    def perform_create(self, serializer):
        # 시리얼라이저야, 저장할 때 poster컬럼은 POST요청자 이름을 넣어
        serializer.save(user=self.request.user)


class MyPostList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=1)


class Category(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs['category'])
