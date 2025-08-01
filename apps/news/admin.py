from django.contrib import admin

from .models import InternalArticle, ExternalArticle, NewsCategory, NewsSource


@admin.register(InternalArticle)
class InternalArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_status', 'published_at', 'category', 'created_at']
    list_filter = ['publication_status', 'category', 'published_at']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ['title']}
    ordering = ['-published_at']
    date_hierarchy = 'published_at'
    filter_horizontal = ['authors']


@admin.register(ExternalArticle)
class ExternalArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source_name', 'publication_status', 'published_at', 'category']
    list_filter = ['publication_status', 'category', 'source_name']
    search_fields = ['title', 'summary', 'content', 'source_name']
    prepopulated_fields = {'slug': ['title']}
    ordering = ['-published_at']
    date_hierarchy = 'published_at'


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ['name']}


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_url', 'scrape_allowed']
    search_fields = ['name', 'base_url']
    list_filter = ['scrape_allowed']
