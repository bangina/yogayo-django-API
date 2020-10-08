
from django.contrib import admin
from django.urls import path, include, re_path
from schema_graph.views import Schema
from posts.views import PostList, PostRetrieveDestroy, CommentList
from diaries.views import DiaryList, DiaryRetrieveDestroy, LikeCreate, ImgUploadView
from users.views import (registration_view)
from bookings.views import LessonList, MyLessonList, LessonUsersList


from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

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
    path('api/get_token/', views.obtain_auth_token),
    path('api/register/', registration_view, name="register"),

    path("api/diaries/", DiaryList.as_view()),
    path("api/diaries/<int:pk>", DiaryRetrieveDestroy.as_view()),
    path("api/diaries/<int:pk>/upload", ImgUploadView.as_view()),
    path("api/diaries/<int:pk>/like", LikeCreate.as_view()),
    path("api/posts/", PostList.as_view()),  # Post 리스트 뷰
    path("api/posts/<int:pk>", PostRetrieveDestroy.as_view()),  # Post 리스트 뷰
    path("api/posts/<int:pk>/comment", CommentList.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api/lessons/<str:date>/', LessonList.as_view()),
    path('api/mylessons/', MyLessonList.as_view()),
    path('api/lesson/<int:lesson>/', LessonUsersList.as_view()),


    # SWAGGER
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
