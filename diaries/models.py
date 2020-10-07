from django.db import models
from users.models import User
from bookings.models import UserLesson
from users.models import GenUser


class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    userLesson = models.ForeignKey(UserLesson, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, null=False)
    mood = models.IntegerField(null=False)
    img_path = models.ImageField(max_length=None, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'diary'
        ordering = ['-created']


class Like(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        GenUser, on_delete=models.CASCADE, default=0)

    class Meta:
        db_table = 'like'
        ordering = ['-created']
