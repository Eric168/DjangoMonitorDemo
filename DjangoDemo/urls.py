"""DjangoDemo URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from demo.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('demo.urls')),
    path('health_check/', health_check, name='health_check'),
]
