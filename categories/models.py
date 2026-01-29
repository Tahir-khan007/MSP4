from django.db import models
from django.conf import settings
from django.utils import timezone


class Category(models.Model):
    """Model for transaction categories."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

    def transaction_count(self):
        """Return the number of transactions in this category."""
        return self.transactions.count()
