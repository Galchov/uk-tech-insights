from django.contrib import admin

from .models import NewsCategory, NewsSource


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_url', 'scrape_allowed']
    search_fields = ['name', 'base_url', 'notes']
    list_filter = ['scrape_allowed']
    ordering = ['name']
