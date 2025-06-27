from django.contrib import admin
from .models import Tutorial, Article


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'estimated_duration', 'created_at', 'updated_at']
    list_filter = ['is_published', 'difficulty', 'tags']
    search_fields = ['title', 'summary', 'content', 'authors']
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ['authors', 'tags']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'created_at', 'updated_at']
    list_filter = ['is_published', 'difficulty', 'tags']
    search_fields = ['title', 'summary', 'content', 'authors']
    prepopulated_fields = {'slug': ['title']}
    filter_horizontal = ['authors', 'tags']
