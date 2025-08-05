from django.db import models
from django.utils.translation import gettext_lazy as _


class Industry(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Industry name'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
    )

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        ordering = ['name']

    def __str__(self):
        return self.name
