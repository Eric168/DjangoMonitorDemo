from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.item_list, name='item_list'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('error-log/', views.error_log, name='error_log'),
    path('http-error/', views.http_error, name='http_error'),
]
