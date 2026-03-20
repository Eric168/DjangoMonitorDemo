from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.item_list, name='item_list'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('error-log/', views.error_log, name='error_log'),
    path('http-error-500/', views.http_error_500, name='http_error_500'),
    path('http-error-404/', views.http_error_404, name='http_error_404'),
    path('health_check/', views.health_check, name='health_check'),
]
