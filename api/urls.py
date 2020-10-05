
from django.contrib import admin
from django.urls import path, include, re_path
from schema_graph.views import Schema
from posts.views import PostList, PostRetrieveDestroy
from diaries.views import DiaryList, DiaryRetrieveDestroy, LikeCreate


from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="YOGAYO OPEN API 명세서",
        default_version='v1',
        description="요가,필라테스 예약 관리 OPEN API 입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("schema/", Schema.as_view()),
    path('admin/', admin.site.urls),
    path("api/diaries/", DiaryList.as_view()),
    path("api/diaries/<int:pk>", DiaryRetrieveDestroy.as_view()),
    path("api/diaries/<int:pk>/like", LikeCreate.as_view()),
    path("api/posts/", PostList.as_view()),  # Post 리스트 뷰
    path("api/posts/<int:pk>", PostRetrieveDestroy.as_view()),  # Post 리스트 뷰
    path('api-auth/', include('rest_framework.urls')),
    path('api/lesson/', include('bookings.urls')),

    # SWAGGER
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
]
# 개발 디버깅 모드에서 업로드된 파일을 다운로드하기 위한 URL주소와 물리경로 설정! /media/파일명.확장자
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
