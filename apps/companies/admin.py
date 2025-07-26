from django.contrib import admin
from .models import Company, Industry


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'foundation_date']
    search_fields = ['name', 'description', 'website']
    list_filter = ['industries', 'operating_countries', 'tech_stack']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['operating_countries', 'industries', 'tech_stack']
    ordering = ['name']


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    ordering = ['name']
