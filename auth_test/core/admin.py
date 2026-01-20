from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомного пользователя с телефонным полем."""

    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Контакты', {'fields': ('email', 'phone')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'phone', 'email', 'password1', 'password2', 'is_active', 'is_staff'),
            },
        ),
    )
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
