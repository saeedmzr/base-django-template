from django.contrib.auth.models import BaseUserManager, Group

from apps.users.enums import UserRoleEnum


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, is_active=True, is_admin=False, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have username')

        user = self.model(
            username=username,
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            **kwargs
        )
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRoleEnum.ADMIN.value)
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields,
        )
        return user
