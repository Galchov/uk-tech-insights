from django.db import models
from django.utils.translation import gettext_lazy as _


class Technology(models.Model):
    name = models.CharField(
        _('technology name'),
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        _('description'),
        blank=True,
    )
    website = models.URLField(
        _('official website'),
        blank=True,
        null=True,
    )
    logo = models.ImageField(
        _('logo'),
        upload_to='technology_logos/',
        blank=True,
        null=True,
        height_field='logo_height',
    )
    logo_height = models.IntegerField(
        editable=False,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('technology')
        verbose_name_plural = _('technologies')

    def __str__(self):
        return self.name
