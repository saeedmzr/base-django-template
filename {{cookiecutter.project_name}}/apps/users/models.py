from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .enums import UserRoleEnum
from ..base.models import BaseModel
from .managers import UserManager
from auditlog.registry import auditlog


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRoleEnum.choices(),
        default=UserRoleEnum.VIEWER.value,
    )
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.role == UserRoleEnum.ADMIN.value

    @property
    def is_superuser(self):
        return self.role == UserRoleEnum.ADMIN.value

auditlog.register(User, exclude_fields=['password', 'updated_at'])

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return f'User ({self.user.username})\'s profile'
