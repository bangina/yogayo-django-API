from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, AdminUser, GenUser
from bookings.models import Lesson, Voucher, VoucherUser, UserLesson
from diaries.models import Diary, Like
from posts.models import Post, Comment

admin.site.register(User, UserAdmin)
admin.site.register(AdminUser)
admin.site.register(GenUser)
admin.site.register(Lesson)
admin.site.register(Voucher)
admin.site.register(VoucherUser)
admin.site.register(UserLesson)
admin.site.register(Diary)
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Comment)
