from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, UserManager as BaseUserManager
# auth_user의 역할을 User가 대신


#
# 커스텀 유저 모델 정의
#
class User(AbstractBaseUser):
    # 상속받아 구현한 필드
    email = models.EmailField(
        max_length=60, unique=True, default="email@gmail.com")
    username = models.CharField(max_length=20, unique=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # 우리가 추가하는 필드
    phone = models.CharField(max_length=11, null=True, unique=True)
    img_profile = models.FileField(upload_to='user', blank=True)

    # 로그인에 사용할(auth) 컬럼 지정.
    USERNAME_FIELD = 'email'
    # 필수 필드 지정
    REQUIRED_FIELDS = ['username', 'phone']

    # 프린트될 내용 세팅
    def __str__(self):
        return self.email + "," + self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Types(models.TextChoices):
        GENUSER = "GENUSER"
        ADMINUSER = "ADMINUSER"

    # 디폴트는 genuser 타입으로 세팅
    # base_type = Types.GENUSER

    # 우리 무슨 유저타입?
    type = models.CharField(max_length=10,
                            choices=Types.choices)
    objects = BaseUserManager()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        # if not self.id:
        #     self.type = self.base_type
        return super().save(*args, **kwargs)

    def create_user(self, email, password,  username):
        if not email:
            raise ValueError("이메일 입력하셔야 합니다")
            if not username:
                raise ValueError("이름 입력하셔야 합니다")
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


#
# 매니저 정의(object.all의 object)
#


class GenUserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.GENUSER)


class AdminUserManager(BaseUserManager):
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


class AdminUser(User):
    base_type = User.Types.ADMINUSER
    objects = AdminUserManager()

    class Meta:
        proxy = True
