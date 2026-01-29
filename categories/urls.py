from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, name='list'),
    path('add/', views.add_category, name='add'),
    path('edit/<int:pk>/', views.edit_category, name='edit'),
    path('delete/<int:pk>/', views.delete_category, name='delete'),
]
