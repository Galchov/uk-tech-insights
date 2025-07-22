from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse


class NewsArticle(models.Model):
    MAX_SLUG_LENGTH = 100

    class PublicationStatus(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        PUBLISHED = 'PUBLISHED', _('Published')
        ARCHIVED = 'ARCHIVED', _('Archived') 

    title = models.CharField(
        max_length=300,
        unique=True,
        verbose_name=_('Article title'),
        help_text=_("The main title of the article.")
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True,
        blank=True,
        verbose_name=_('Slug'),
        help_text=_("Automatically generated from the title. Used in URL."),
    )
    summary = models.TextField(
        blank=True,
        verbose_name=_('Summary'),
        help_text=_("Short summary for the article."),
    )
    content = models.TextField(
        verbose_name=_('Main content'),
        help_text=_("The actual news content."),
    )
    cover_image = models.ImageField(
        upload_to='news_covers/',
        blank=True,
        null=True,
        verbose_name=_('Cover image'),
        help_text=_("Displayed on the top of the news article."),
    )
    authors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='news_articles',
        blank=True,
        verbose_name=_('Article authors'),
        help_text=_("Users credited as authors."),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
        help_text=_("Date and time when the article was created."),
    )
    publication_status = models.CharField(
        max_length=30,
        choices=PublicationStatus,
        default=PublicationStatus.DRAFT,
        db_index=True,
        verbose_name=_("Publication status"),
        help_text=_("Current status of the article."),
    )
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Published at'),
        help_text=_("Date and time of publication."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
        help_text=_("Date and time of update."),
    )
    category = models.ForeignKey(
        to='NewsCategory',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Article category'),
        help_text=_("One category per article."),
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("View count"),
        help_text=_("Number of times the article has been viewed."),
    )
    source_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('External source name'),
        help_text=_("Name of the original source if this article was scraped or referenced from another website. Not registered.")
    )
    source_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Source URL'),
        help_text=_("URL of the original source if this article was scraped or referenced from another website. Not registered."),
    )
    source = models.ForeignKey(
        to='NewsSource',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='articles',
        verbose_name=_('Source'),
        help_text=_("Structured reference to a known registered source."),
    )

    class Meta:
        verbose_name = _('News Article')
        verbose_name_plural = _('News Articles')
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
            base_slug = slugify(self.title).lower()[:self.MAX_SLUG_LENGTH]
            slug = base_slug
            counter = 1

            while NewsArticle.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                suffix = f"-{counter}"
                allowed_length = self.MAX_SLUG_LENGTH - len(suffix)
                slug = f"{base_slug[:allowed_length]}{suffix}"
                counter += 1

            self.slug = slug

        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={'slug': self.slug})


class NewsCategory(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name=_('Category name'),
        help_text=_("News article category."),
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_('Slug'),
        help_text=_("Slug if needed for category modification."),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_("Description of the category. Optional."),
    )

    class Meta:
        verbose_name = _("News Category")
        verbose_name_plural = _("News Categories")
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name).lower()
            slug = base_slug
            counter = 1

            while NewsCategory.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:category_detail', kwargs={'slug': self.slug})


class NewsSource(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Source name'),
        help_text=_("Name of the article source."),
    )
    base_url = models.URLField(
        verbose_name=_('Source URL'),
        help_text=_("URL of the article source."),
    )
    scrape_allowed = models.BooleanField(
        default=False,
        verbose_name=_('Scrape allowed'),
        help_text=_("Indicates whether it is allowed to scrape from that particular source."),
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes'),
        help_text=_("Additional information about the source. Optional."),
    )

    class Meta:
        verbose_name = _("News Source")
        verbose_name_plural = _("News Sources")
        ordering = ['name']

    def __str__(self):
        return self.name
    