from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Tutorial, Article, TutorialCompletion, Category
from apps.common.models import Comment, Star, TaggedItem


class TutorialCompletionInLine(admin.TabularInline):
    model = TutorialCompletion
    extra = 0
    readonly_fields = ['user', 'completed_at']


class CommentInLine(GenericTabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['user', 'content']


class StarInLine(GenericTabularInline):
    model = Star
    extra = 0


class TaggedItemInLine(GenericTabularInline):
    model = TaggedItem
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
    ordering = ['name']


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'difficulty', 'estimated_duration', 'created_at', 'updated_at']
    list_filter = ['is_published', 'difficulty', 'tags', 'categories']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ['authors', 'categories']
    inlines = [TutorialCompletionInLine, CommentInLine]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'difficulty', 'created_at', 'updated_at']
    list_filter = ['is_published', 'difficulty', 'tags', 'categories']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ['authors', 'categories']
    inlines = [CommentInLine, StarInLine, TaggedItemInLine]


@admin.register(TutorialCompletion)
class TutorialComletionAdmin(admin.ModelAdmin):
    list_display = ['user', 'tutorial', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['user__email', 'tutorial__title']
