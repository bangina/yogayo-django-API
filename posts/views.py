from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):  # 뷰 기반의 클래스 생성
    queryset = Post.objects.all()  # DB에서 쿼리셋 전부 가져왕
    serializer_class = PostSerializer
    # IsAuthenticated:로그인유저만 /IsAuthenticatedOrReadOnly: 로그인유저는 post가능,아니면 readonly
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 예약어임
    def perform_create(self, serializer):
        # 시리얼라이저야, 저장할 때 poster컬럼은 POST요청자 이름을 넣어
        serializer.save(poster=self.request.user)


# class PostDetail(DetailView):
