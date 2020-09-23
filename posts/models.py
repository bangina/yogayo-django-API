from django.db import models
from django.db import models
from django.contrib.auth.models import User
from users.models import User
from users.models import GenUser


class Post(models.Model):
    user = models.ForeignKey(GenUser, on_delete=models.CASCADE)

    class Types(models.TextChoices):
        # 코드 내에서 불러오는 값 = "DB에 저장되는 값", "admin에서 표시되는 값"
        SECONDHAND = "SECONDHAND", "중고장터"
        YOGA = "YOGA", "요가"
        PILATES = "PILATES", "필라테스"
        MEETUP = "MEETUP", "같이 운동해요"
        ETC = "ETC", "기타"

    category = models.CharField(
        max_length=10, null=False, choices=Types.choices)
    title = models.CharField(max_length=100, null=False)
    content = models.CharField(max_length=2000, null=False)
    img_path = models.FileField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'post'
        ordering = ['-created']


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)
    user = models.ForeignKey(GenUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=500,  null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
        ordering = ['-created']
