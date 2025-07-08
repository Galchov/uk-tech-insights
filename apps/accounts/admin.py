from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from .models import CustomUser, Profile
from .forms import CustomRegistrationForm, CustomUserChangeForm


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'
    fk_name = 'user'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomRegistrationForm
    form = CustomUserChangeForm
    model = CustomUser

    inlines = [ProfileInLine]

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

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        
        return super().get_inline_instances(request, obj)


admin.site.register(Permission)
