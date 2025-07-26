from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Country'),
    )

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('City'),
    )
    country = models.ForeignKey(
        to=Country,
        on_delete=models.CASCADE,
        related_name='cities',
    )

    class Meta:
        unique_together = ['name', 'country']

    def __str__(self):
        return f"{self.name}, {self.country.name}"
