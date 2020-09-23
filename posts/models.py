from django.db import models
from django.db import models
from django.contrib.auth.models import User
from users.models import User
from users.models import GenUser


class Post(models.Model):
    user = models.ForeignKey(GenUser, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=100, null=False)
    content = models.CharField(max_length=2000, null=False)
    img_path = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'post'
        ordering = ['-created']


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=500,  null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
        ordering = ['-created']
