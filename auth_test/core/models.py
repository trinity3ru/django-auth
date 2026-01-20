from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Менеджер пользователя, гарантирующий корректный телефон и email."""

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('username is required')
         
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    """Расширенная модель пользователя с необязательным телефоном и обязательным email."""

    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text='Телефон не обязателен.',
    )
    email = models.EmailField(
        unique=True,
        help_text='Email обязателен, используется для уведомлений.',
    )

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} ({self.phone})'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
