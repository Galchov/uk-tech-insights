from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('email_address'),
        unique=True,
        help_text=_('Enter a valid email address. This will be used to log in.'),
    )
    email_verified = models.BooleanField(
        _('email verified'),
        default=False,
        help_text=_('Indicates whether the user has verified their email address.'),
    )
    bio = models.TextField(
        _('biography'),
        blank=True,
        null=True,
        help_text=_('Optional: Write a short bio to display on your profile.'),
    )
    country = models.CharField(
        _('country of residence'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Optional: Your current country of residence.'),
    )
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text=_('Optional: Upload a profile image.'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        self.email = self.email.lower()
        super().save(*args, **kwargs)
    