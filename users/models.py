from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None

    email = models.EmailField(null=True, blank=True, verbose_name='Почта', unique=True)
    tg_id = models.BigIntegerField(verbose_name='Телеграмм', unique=True)
    phone = models.CharField(null=True, blank=True, max_length=150, verbose_name='Телефон')

    """avatar = models.ImageField(null=True, blank=True, verbose_name='Аватар')
    country = models.CharField(null=True, blank=True, max_length=150, verbose_name='Страна')

    token = models.CharField(null=True, blank=True, max_length=150, verbose_name='Token')
"""

    USERNAME_FIELD = 'tg_id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):

        if self.first_name and self.last_name:
            return f'USER: {self.first_name} {self.last_name}'
        else:
            return f'USER: {self.tg_id}'
