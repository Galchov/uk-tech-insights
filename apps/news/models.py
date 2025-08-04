import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from .slug import generate_unique_slug
from apps.common.models import Comment, Star, TaggedItem


class BaseArticle(models.Model):
    SLUG_MAX_LENGTH = 300

    class ArticleType(models.TextChoices):
        INTERNAL = 'INTERNAL', _('Internal')
        EXTERNAL = 'EXTERNAL', _('External')

    class PublicationStatus(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        PUBLISHED = 'PUBLISHED', _('Published')
        ARCHIVED = 'ARCHIVED', _('Archived')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'),
    )
    article_type = models.CharField(
        max_length=20,
        choices=ArticleType.choices,
        editable=False,
        db_index=True,
    )
    title = models.CharField(
        max_length=300,
        unique=True,
        verbose_name=_('News article title'),
    )
    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
        blank=True,
        verbose_name=_('Automatically generated from the title'),
    )
    summary = models.TextField(
        blank=True,
        verbose_name=_('News article summary'),
    )
    content = models.TextField(
        verbose_name=_('News article content'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date and time of creation'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Date and time of last update'),
    )
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Date and time of publication'),
    )
    publication_status = models.CharField(
        max_length=30,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
        db_index=True,
        verbose_name=_('Publication status'),
    )
    category = models.ForeignKey(
        to='NewsCategory',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Category'),
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Views count'),
    )
    comments = GenericRelation(Comment)
    stars = GenericRelation(Star)
    tags = GenericRelation(TaggedItem)

    class Meta:
        abstract = True
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['publication_status']),
            models.Index(fields=['published_at']),
        ]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(
                instance=self,
                field_value=self.title,
                slug_field_name='slug',
                max_length=self._meta.get_field('slug').max_length,
                suffix_length=6,
            )

        super().save(*args, **kwargs)


class InternalArticle(BaseArticle):
    authors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        blank=True,
        related_name='internal_articles',
        verbose_name=_('News article authors'),
    )
    cover_image = models.ImageField(
        upload_to='news_covers/',
        blank=True,
        null=True,
        verbose_name=_('News article poster'),
    )

    class Meta:
        verbose_name = _('Internal Article')
        verbose_name_plural = _('Internal Articles')

    def save(self, *args, **kwargs):
        if not self.article_type:
            self.article_type = self.ArticleType.INTERNAL
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:internal_article_detail', kwargs={'slug': self.slug})


class ExternalArticle(BaseArticle):
    image_url = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_('URL to image'),
    )
    source_name = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_('Source name'),
    )
    source_url = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_('Source URL'),
    )
    source = models.ForeignKey(
        to='NewsSource',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='external_sources',
        verbose_name=_('Source object'),
    )
    author = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Author'),
    )

    class Meta:
        verbose_name = _('External Article')
        verbose_name_plural = _('External Articles')

    def save(self, *args, **kwargs):
        if not self.article_type:
            self.article_type = self.ArticleType.EXTERNAL
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:external_article_detail', kwargs={'slug': self.slug})
    

class NewsCategory(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name=_('Name'),
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_('Automatically generated from the name'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
    )

    class Meta:
        verbose_name = _('News Category')
        verbose_name_plural = _('News Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while NewsCategory.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug

        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:category_detail', kwargs={'slug': self.slug})


class NewsSource(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name=_('Name'),
    )
    base_url = models.URLField(
        verbose_name=_('Source URL'),
    )
    scrape_allowed = models.BooleanField(
        default=False,
        verbose_name=_('Scrape allowed'),
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes'),
    )

    class Meta:
        verbose_name = _("News Source")
        verbose_name_plural = _("News Sources")
        ordering = ['name']

    def __str__(self):
        return self.name
