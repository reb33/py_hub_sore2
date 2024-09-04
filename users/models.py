from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True, null=True, verbose_name="аватар")

    class Meta:
        db_table = 'user'
        verbose_name = "Пользователя"  # оторажение в админке
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username  # оторажение в админке
