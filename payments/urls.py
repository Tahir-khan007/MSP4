from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('upgrade/', views.upgrade_view, name='upgrade'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='webhook'),
]
