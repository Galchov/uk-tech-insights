from django.contrib import admin

from .models import Industry


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    ordering = ['name']
