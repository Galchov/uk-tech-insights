from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import F

from apps.common.models import TaggedItem, Comment, Star


class ForumPost(models.Model):
    title = models.CharField(
        _('post title'),
        max_length=255,
        help_text=_("The main heading for the post."),
    )
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        unique=True,
        blank=True,
        help_text=_("Automatically generated from the title. Used in URL."),
    )
    content = models.TextField(
        _('content'),
        help_text=_("Main body of the post."),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_posts',
        verbose_name=_('author'),
    )
    category = models.ForeignKey(
        'ForumCategory',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name=_('category'),
    )
    is_published = models.BooleanField(
        _('published'),
        default=True,
    )
    is_pinned = models.BooleanField(
        _('pinned'),
        default=False,
    )
    is_closed = models.BooleanField(
        _('closed'),
        default=False,
    )
    views = models.PositiveIntegerField(
        _('views'),
        default=0,
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('last updated'),
        auto_now=True,
    )

    comments = GenericRelation(Comment)
    stars = GenericRelation(Star)
    tags = GenericRelation(TaggedItem)

    class Meta:
        ordering = ['-is_pinned', '-created_at']
        verbose_name = _('forum post')
        verbose_name_plural = _('forum posts')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug

            counter = 1
            while ForumPost.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = unique_slug

        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('forum:post_details', kwargs={'slug': self.slug})
    
    def increment_views(self):
        ForumPost.objects.filter(pk=self.pk).update(views=F('views') + 1)
        self.refresh_from_db(fields=['views'])
    

class ForumCategory(models.Model):
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=150,
        unique=True,
    )
    description = models.TextField(
        _('description'),
        blank=True,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='subcategories',
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('forum category')
        verbose_name_plural = _('forum categories')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug

            counter = 1
            while ForumCategory.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = unique_slug

        super().save(*args, **kwargs)
