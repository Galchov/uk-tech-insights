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
    location = models.ForeignKey(
        to='locations.City',
        on_delete=models.SET_NULL,
        null=True,
        related_name='companies',
        verbose_name='Headquarters Location',
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Company Address',
    )
    operating_countries = models.ManyToManyField(
        to='locations.Country',
        related_name='operating_companies',
        verbose_name='Operating Countries',
        blank=True,
    )
    industries = models.ManyToManyField(
        to='Industry',
        related_name='companies',
        verbose_name=_('Industry'),
        help_text=_("Company can cover multiple areas of operation."),
        blank=True,
    )
    tech_stack = models.ManyToManyField(
        to='technologies.Technology',
        related_name='companies',
        verbose_name=_('Tech stack'),
        help_text=_("The tech stack company uses for their services."),
        blank=True,
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
    
    @property
    def formatted_foundation_date(self):
        """Formatted to display month's name and the year"""

        if self.foundation_date:
            return self.foundation_date.strftime("%B %Y")
        return "Not available"


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
