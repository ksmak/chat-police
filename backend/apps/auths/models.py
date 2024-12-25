from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, username, ip, name, password=None):
        if not username:
            raise ValidationError("Логин не должен быть пустым.")

        if not ip:
            raise ValidationError("ip-адрес не должен быть пустым.")

        if not name:
            raise ValidationError("Имя не должно быть пустым.")

        user = self.model(username=username, ip=ip, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, ip, name, password=None):
        user = self.create_user(username=username, ip=ip, name=name, password=password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    username = models.CharField(verbose_name="логин", max_length=50, unique=True)
    ip = models.GenericIPAddressField(verbose_name="ip-адрес", unique=True)
    name = models.CharField(verbose_name="имя", max_length=255)
    is_active = models.BooleanField(verbose_name="активность", default=True)
    is_superuser = models.BooleanField(verbose_name="администратор", default=False)
    is_staff = models.BooleanField(verbose_name="штатный сотрудник", default=False)
    created_at = models.DateTimeField(verbose_name="создан", auto_now_add=True)
    changed_at = models.DateTimeField(verbose_name="изменен", auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["ip", "name"]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
