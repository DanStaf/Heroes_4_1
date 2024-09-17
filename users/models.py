from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='Почта', unique=True)
    tg_id = models.BigIntegerField(null=True, blank=True, verbose_name='Телеграмм')

    """avatar = models.ImageField(null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(null=True, blank=True, max_length=150, verbose_name='Телефон')
    country = models.CharField(null=True, blank=True, max_length=150, verbose_name='Страна')

    token = models.CharField(null=True, blank=True, max_length=150, verbose_name='Token')
"""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):

        if self.first_name and self.last_name:
            return f'USER: {self.first_name} {self.last_name}'
        else:
            return f'USER: {self.email}'
