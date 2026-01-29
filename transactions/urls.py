from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('add/', views.add_transaction, name='add'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete'),
]
