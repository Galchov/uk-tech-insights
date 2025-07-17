from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

from apps.common.models import Comment, Star, TaggedItem


class BaseLearningContent(models.Model):
    class DifficultyLevels(models.TextChoices):
        BEGINNER = 'BEGINNER', _('Beginner')
        INTERMEDIATE = 'INTERMEDIATE', _('Intermediate')
        ADVANCED = 'ADVANCED', _('Advanced')

    title = models.CharField(
        _('title'),
        max_length=200,
        help_text=_("The main heading for the content"),
    )
    cover_image = models.ImageField(
        _('cover image'),
        upload_to='tutorial_covers/',
        blank=True,
        null=True,
        help_text=_("Displayed at the top of the tutorial or article."),
    )
    slug = models.SlugField(
        _('slug'),
        max_length=220,
        unique=True,
        blank=True,
        help_text=_("Automatically generated from the title. Used in the ULR."),
    )
    summary = models.TextField(
        _('summary'),
        max_length=500,
        help_text=_("A short summary shown in listings or previews."),
    )
    content = models.TextField(
        _('content'),
        help_text=_("Main body of the content. Supports markdown or rich text with code blocks."),
    )
    difficulty = models.CharField(
        _('difficulty'),
        max_length=20,
        choices=DifficultyLevels,
        default='Not provided',
        help_text=_("Select the intended difficulty level for this content."),
    )
    estimated_duration = models.PositiveIntegerField(
        _('estimated duration in minutes'),
        blank=True,
        null=True,
        help_text=_("Estimated time to complete/read."),
    )
    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='%(class)ss',
        verbose_name=_('authors'),
        help_text=_("Users credited as authors.")
    )
    is_published = models.BooleanField(
        _('is published'),
        default=False,
        help_text=_("Control whether the content is publicly visible."),
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True,
    )
    views = models.PositiveIntegerField(
        _('views'),
        default=0,
    )
    
    comments = GenericRelation(Comment)
    stars = GenericRelation(Star)
    tags = GenericRelation(TaggedItem)

    class Meta:
        abstract = True
        ordering = ['-created_at']
        get_latest_by = 'created_at'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = _('learning content')
        verbose_name_plural = _('learning contents')
    
    def __str__(self):
        return self.title + '\n' + self.summary
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            ModelClass = self.__class__

            counter = 1
            while ModelClass.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)


class Tutorial(BaseLearningContent):
    categories = models.ManyToManyField(
        'Category',
        blank=True,
        related_name='tutorials',
    )

    class Meta:
        verbose_name = _('tutorial')
        verbose_name_plural = _('tutorials')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]
        permissions = [
            ('can_publish_tutorials', "Can publish tutorials"),
            ('can_edit_others_tutorials', "Can edit others' tutorials"),
        ]

    def get_absolute_url(self):
        return reverse('learning:tutorial_detail', kwargs={'slug': self.slug})


class TutorialCompletion(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    tutorial = models.ForeignKey(
        Tutorial,
        on_delete=models.CASCADE,
    )
    completed_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ['user', 'tutorial']
        verbose_name = _('tutorial completion')
        verbose_name_plural = _('tutorial completions')

    def __str__(self):
        return f"{self.user} has completed {self.tutorial}"
    

class Article(BaseLearningContent):
    categories = models.ManyToManyField(
        'Category',
        blank=True,
        related_name='articles',
    )
    
    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]

    def get_absolute_url(self):
        return reverse('learning:article_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=200,
        unique=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1

            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = unique_slug
        
        super().save(*args, **kwargs)
