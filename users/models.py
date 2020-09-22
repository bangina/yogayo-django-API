from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
# auth_user의 역할을 User가 대신


#
# 커스텀 유저 모델 정의
#
class User(AbstractUser):
    phone = models.CharField(max_length=11, null=True)

    class Types(models.TextChoices):
        GENUSER = "GENUSER", "GenUser"
        ADMINUSER = "ADMINUSER", "AdminUser"

    base_type = Types.GENUSER

    # 우리 무슨 유저타입?
    type = models.CharField(max_length=10,
                            choices=Types.choices, default=base_type)


name = models.CharField(blank=True, max_length=255)


def get_absolute_url(self):
    return reverse("users:detail", kwargs={"pk": self.pk})


def save(self, *args, **kwargs):
    if not self.id:
        self.type = self.base_type
    return super().save(*args, **kwargs)


#
# 매니저 정의(object.all의 object)
#

class GenUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.GENUSER)


class AdminUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ADMINUSER)


#
# proxy 모델 정의
# 

class GenUser(User):
    base_type = User.Types.GENUSER
    objects = GenUserManager()

    class Meta:
        proxy = True

    # 유저 권한 정의 여기다 하면될까?
    # def whisper(self):
    #     return "whisper"


class AdminUser(User):
    base_type = User.Types.ADMINUSER
    objects = AdminUserManager()

    class Meta:
        proxy = True

    # 유저 권한 정의 여기다 하면될까?
    # def whisper(self):
    #     return "whisper"
