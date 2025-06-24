from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomRegistrationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomRegistrationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['username', 'email', 'is_staff', 'is_active']

    fieldsets = [
        (
            None,
            {
                "fields": ['email', 'username', 'password'],
            },
        ),
        (
            "Personal Information",
            {
                "fields": ['first_name', 'last_name'],
            },
        ),
        (
            "Permissions",
            {
                "fields": ['is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'],
            },
        ),
        (
            "Important Dates",
            {
                "fields": ['last_login', 'date_joined'],
            },
        ),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ['wide'],
                "fields": ['email', 'username', 'password1', 'password2', 'is_staff', 'is_active'],
            },
        ),
    ]

    search_fields = ['email', 'username']
    ordering = ['email']
