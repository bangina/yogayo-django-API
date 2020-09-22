from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, AdminUser, GenUser


admin.site.register(User)
admin.site.register(AdminUser)
admin.site.register(GenUser)
