from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for Payment model."""
    list_display = ['user', 'amount', 'status', 'stripe_payment_id', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'stripe_payment_id']
    ordering = ['-created_at']
    readonly_fields = ['stripe_payment_id', 'created_at', 'updated_at']
