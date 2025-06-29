from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.conf import settings

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Enter a valid email address. This will be used to log in.'),
    )
    email_verified = models.BooleanField(
        _('email verified'),
        default=False,
        help_text=_('Indicates whether the user has verified their email address.'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        self.email = self.email.lower()
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('user')
    )
    headline = models.CharField(
        _('headline'),
        blank=True,
        help_text=_("Optional: A short tagline or headline summarizing your professional identity."),
    )
    bio = models.TextField(
        _('biography'),
        blank=True,
        help_text=_('Optional: Write a short bio to display on your profile.'),
    )
    date_of_birth = models.DateField(
        _('date of birth'),
        blank=True,
        null=True,
        help_text=_("Optional: Your birth date."),
    )
    city = models.CharField(
        _('city'),
        max_length=100,
        blank=True,
        help_text=_('Your city of residence.'),
    )
    country = CountryField(
        _('country of residence'),
        blank=True,
        blank_label='(Select country)',
        help_text=_('Your current country of residence.'),
    )
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text=_('Optional: Upload a profile image.'),
    )

    personal_website = models.URLField(
        _('personal website'),
        blank=True,
        null=True,
        help_text=_("Optional: Your personal/portfolio website."),
    )
    linkedin = models.URLField(
        _('LinkedIn'),
        blank=True,
        null=True,
        help_text=_("Optional: Your LinkedIn profile."),
    )
    twitter = models.URLField(
        _('Twitter'),
        blank=True,
        null=True,
        help_text=_("Optional: You Twitter profile.")
    )
    github = models.URLField(
        _('GitHub'),
        blank=True,
        null=True,
        help_text=_("Optional: Your GitHub profile."),
    )
    gitlab = models.URLField(
        _('GitLab'),
        blank=True,
        null=True,
        help_text=_("Optional: Your GitLab profile."),
    )

    tech_stack = models.ManyToManyField(
        'technologies.Technology',
        blank=True,
        help_text=_("Your tech stack."),
    )
    contact_email = models.EmailField(
        _('contact email'),
        blank=True,
        null=True,
        help_text=_("Optional: Public email for professional contacts."),
    )
    languages = models.CharField(
        _('languages'),
        max_length=255,
        blank=True,
        help_text=_("Optional: Languages you speak (e.g., English, Spanish)."),
    )

    def __str__(self) -> str:
        return f"Profile of {self.user.username}"
