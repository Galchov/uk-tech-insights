from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'foundation_date']
    search_fields = ['name', 'description', 'website']
    list_filter = ['industries', 'operating_countries', 'tech_stack']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['operating_countries', 'industries', 'tech_stack']
    ordering = ['name']
