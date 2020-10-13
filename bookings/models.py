from django.db import models
from django.conf import settings
from users.models import User
from users.models import AdminUser
from users.models import GenUser


class Lesson(models.Model):
    user = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    room = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    max_ppl = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'lesson'
        ordering = ['-time']


class Voucher(models.Model):
    # adminUser(센터)
    user = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'voucher'


class VoucherUser(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    user = models.ForeignKey(GenUser, on_delete=models.CASCADE)
    str_date = models.DateTimeField(auto_now_add=True)
    used = models.IntegerField(blank=True, default=0)  # 바우처 수업 사용횟수
    status = models.BooleanField(blank=True, default=True)  # 정상/만료

    class Meta:
        db_table = 'voucher_user'


class UserLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(GenUser, on_delete=models.CASCADE)
    voucher = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=20, blank=True, null=True)
    room = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    max_ppl = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user_lesson'
        ordering = ['-time']
