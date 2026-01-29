from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Adds premium membership functionality for paid features.
    """
    email = models.EmailField(unique=True)
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_active_premium(self):
        """Check if user has an active premium subscription."""
        if not self.is_premium:
            return False
        if self.premium_until is None:
            return False
        return self.premium_until > timezone.now()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
