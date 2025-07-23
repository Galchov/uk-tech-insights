from django.contrib import admin
from .models import Company, Location, Industry


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'headquarters', 'website', 'foundation_date']
    search_fields = ['name', 'description', 'website']
    list_filter = ['industries', 'operating_countries', 'tech_stack']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['operating_countries', 'industries', 'tech_stack']
    ordering = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['country', 'city', 'address']
    search_fields = ['country', 'city', 'address']
    ordering = ['country', 'city']


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
    ordering = ['name']
