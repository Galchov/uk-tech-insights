from django.contrib import admin
from .models import ForumPost, ForumCategory


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'is_pinned', 'is_closed', 'views', 'created_at', 'updated_at']
    list_filter = ['is_published', 'is_pinned', 'is_closed', 'category']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ['title']}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    ordering = ['-is_pinned', '-created_at']


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ['name']}
