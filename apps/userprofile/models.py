
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Переопределение модели пользователь"""

    CHOICES_GENDER = [
        ('male', 'male'),
        ('female', 'female')
    ]

    gender = models.CharField(max_length=6, choices=CHOICES_GENDER, verbose_name='Пол')
    phone = models.CharField(max_length=25, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='avatars', verbose_name='Аватарка')

    def __str__(self):
        return f'{self.pk}, {self.first_name}, {self.last_name}, {self.gender}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'