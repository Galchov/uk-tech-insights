from django.contrib import admin

from .models import NewsArticle, NewsCategory, NewsSource


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'publication_status',
        'published_at',
        'view_count',
        'source',
    ]
    list_filter = [
        'publication_status',
        'category',
        'created_at',
        'published_at',
        'source',
    ]
    search_fields = [
        'title',
        'summary',
        'content',
        'source_name',
        'source_url',
    ]
    autocomplete_fields = ['category', 'source', 'authors']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['authors']
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'summary', 'content', 'cover_image',
            )
        }),
        ('Publication', {
            'fields': (
                'publication_status', 'published_at', 'view_count',
            )
        }),
        ('Relations', {
            'fields': (
                'category', 'authors',
            )
        }),
        ('Source', {
            'fields': (
                'source', 'source_name', 'source_url',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


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
