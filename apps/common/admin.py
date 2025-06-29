from django.contrib import admin
from .models import Tag, TaggedItem, Comment, Star


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ['tag', 'content_object', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_object', 'created_at']
    search_fields = ['content']


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_object', 'starred_at']
    readonly_fields = ['starred_at']
