from django.shortcuts import render
from rest_framework import generics, permissions

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by(
        '-created')  # DB에서 쿼리셋 전부 가져왕
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # 시리얼라이저야, 저장할 때 poster컬럼은 POST요청자 이름을 넣어
        serializer.save(user=self.request.user)


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 작성자만 삭제가능

    # 삭제하는 함수
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(
            pk=self.kwargs['pk'], user=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("그쪽 게시물이 아닌데용!!! 못 지우세요!!")
