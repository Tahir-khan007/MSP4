from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser model."""
    model = CustomUser
    list_display = ['email', 'username', 'is_premium', 'premium_until', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_premium', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['-created_at']

    fieldsets = UserAdmin.fieldsets + (
        ('Premium Status', {
            'fields': ('is_premium', 'premium_until', 'stripe_customer_id')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Premium Status', {
            'fields': ('is_premium', 'premium_until')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
