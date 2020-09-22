from django.db import models
from users.models import User
from bookings.models import UserLesson


class Diary(models.Model):
    userLesson = models.ForeignKey(UserLesson, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, null=False)
    mood = models.IntegerField(null=False)
    img_path = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'diary'
        ordering = ['-created']


class Like(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'like'
        ordering = ['-created']
