from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name=_('Name'),
        help_text=_("Company's name."),
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name=_('Slug'),
        help_text=_("Automatically generated from the name. Used in the URL."),
    )
    logo = models.ImageField(
        upload_to='company_logo/',
        blank=True,
        null=True,
        verbose_name=_('Logo'),
        help_text=_("Company's logo."),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_("Summarized information about the company."),
    )
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Website'),
        help_text=_("Company's official website."),
    )
    foundation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Foundation date'),
        help_text=_("Date the company was founded."),
    )
    headquarters = models.ForeignKey(
        to='Location',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Headquarters'),
        help_text=_("Company's head office."),
    )
    operating_countries = models.ManyToManyField(
        to='Location',
        related_name='companies_operating',
        verbose_name=_('Countries of operation'),
        help_text=_("Company can have businesses in multiple countries."),
    )
    industries = models.ManyToManyField(
        to='Industry',
        related_name='companies',
        verbose_name=_('Industry'),
        help_text=_("Company can cover multiple areas of operation."),
    )
    tech_stack = models.ManyToManyField(
        to='technologies.Technology',
        related_name='companies',
        verbose_name=_('Tech stack'),
        help_text=_("The tech stack company uses for their services."),
    )

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            num = 1

            while Company.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('companies:company_detail', kwargs={'slug': self.slug})


class Location(models.Model):
    country = models.CharField(
        max_length=60,
        verbose_name=_('Country'),
    )
    city = models.CharField(
        max_length=60,
        blank=True,
        verbose_name=_('City'),
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Address'),
    )

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['country', 'city']

    def __str__(self):
        return f"{self.city}, {self.country}" if self.city else self.country


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
