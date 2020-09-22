from django.db import models
from django.conf import settings
from users.models import User


class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # studio_id = models.CharField(max_length=20)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'voucher'


class UserLesson(models.Model):
    lesson = models.ForeignKey(Lesson,  on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # voucher 삭제되면 얘도 삭제되는게 맞나? 바우처 포린키 없어도 되지?
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    room = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    max_ppl = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user_lesson'
        ordering = ['-time']


class VoucherUser(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    str_date = models.DateTimeField(auto_now_add=True)
    # end_date = models.DateField(blank=True, null=True) ##보관할 데이터 아니고 계산해야 하는 데이터니까 컬럼 필요없지 않을까?
    used = models.IntegerField(blank=True, default=0)  # 바우처 수업 사용횟수
    status = models.BooleanField(blank=True, default=True)  # 정상/만료

    class Meta:
        db_table = 'voucher_user'
