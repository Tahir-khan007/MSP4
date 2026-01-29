from django.db import models
from django.conf import settings
from django.utils import timezone
from categories.models import Category


class Transaction(models.Model):
    """Model for financial transactions."""
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-date']),  # For filtering user transactions by date
            models.Index(fields=['user', 'transaction_type']),  # For filtering by type
            models.Index(fields=['category']),  # For category lookups
        ]

    def __str__(self):
        return f'{self.description} - £{self.amount}'
