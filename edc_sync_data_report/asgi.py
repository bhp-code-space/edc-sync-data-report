"""
<<<<<<< HEAD
ASGI config for edc_sync_data_report project.
=======
ASGI config for mysite project.
>>>>>>> fd8d3ec90dbac6a5afd7e14fdf4d2b280017863c

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
=======
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
>>>>>>> fd8d3ec90dbac6a5afd7e14fdf4d2b280017863c
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edc_sync_data_report.settings')

application = get_asgi_application()
