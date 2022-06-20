from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.postgres.fields import CICharField, CIEmailField

class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = CICharField(
        max_length=15,
        unique=True,
        error_messages={'unique': 'Данное имя уже занято. Пожалуйста, выберите другое.'},
        verbose_name='Username',
    )
    email = CIEmailField(
        max_length=255,
        unique=True,
        error_messages={'unique': 'Адрес электронной почты уже занят.'},
        verbose_name='Email'
    )
    profile_name = models.CharField(max_length=50, verbose_name='Имя профиля')
    about = models.CharField(max_length=160, blank=True, verbose_name='О себе')
    location = models.CharField(max_length=30, blank=True, verbose_name='Местоположение')
    website = models.URLField(max_length=100, blank=True, verbose_name='Веб-сайт')
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'profile_name', 'date_of_birth']

    def get_short_name(self):
        return self.username
