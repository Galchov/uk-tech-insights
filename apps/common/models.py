from uuid import UUID
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=100,
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
    

class TaggedItem(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tagged_items',
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ['tag', 'content_type', 'object_id']
        verbose_name = _('tagged item')
        verbose_name_plural = _('tagged items')

    def __str__(self):
        return f"{self.tag.name} >> {self.content_object}"


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.TextField()
    content_object = GenericForeignKey()

    content = models.TextField(
        _('actual comment'),
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='replies',
        help_text=_("Reply to another comment.")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return f"Comment by {self.user} on {self.content_object}"
    

class Star(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stars',
        verbose_name=_('user'),
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    starred_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        ordering = ['-starred_at']
        verbose_name = _('star')
        verbose_name_plural = _('stars')

    def __str__(self):
        return f"{self.user} starred {self.content_object}"
