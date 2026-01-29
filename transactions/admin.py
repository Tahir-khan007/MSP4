from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for Transaction model."""
    list_display = ['description', 'user', 'category', 'amount', 'transaction_type', 'date', 'created_at']
    list_filter = ['transaction_type', 'date', 'category', 'user']
    search_fields = ['description', 'user__email', 'category__name']
    ordering = ['-date', '-created_at']
    date_hierarchy = 'date'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'category')
