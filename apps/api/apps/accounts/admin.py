# apps/api/apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model"""
    
    list_display = ('phone', 'first_name', 'gender', 'age', 'is_phone_verified', 'created_at')
    list_filter = ('is_phone_verified', 'gender', 'is_staff', 'is_active', 'created_at')
    search_fields = ('phone', 'first_name', 'email')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Şəxsi məlumatlar'), {'fields': (
            'first_name', 'last_name', 'email', 'gender', 'birth_date'
        )}),
        (_('Təsdiqləmə'), {'fields': (
            'is_phone_verified', 'otp_code', 'otp_created_at', 'otp_attempts'
        )}),
        (_('İcazələr'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
        )}),
        (_('Vaxtlar'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone', 'first_name', 'gender', 'birth_date',
                'password1', 'password2', 'is_staff', 'is_active'
            ),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'age')