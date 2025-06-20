from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        _('email_address'),
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        self.email = self.email.lower()
        super().save(*args, **kwargs)
    