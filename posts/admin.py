from django.contrib import admin
from posts.models import Post, Comment


#admin사이트에서 views 필드 읽기전용으로 보이게 하기
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('views',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
