"""WSGI config for DjangoDemo project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoDemo.settings')

application = get_wsgi_application()
