from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ['name', 'user', 'transaction_count', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'user__email']
    ordering = ['name']

    def transaction_count(self, obj):
        return obj.transaction_count()
    transaction_count.short_description = 'Transactions'
