"""WSGI config for CarConnectivity WebUI plugin."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carconnectivity_plugins.webui.django_app.settings')

application = get_wsgi_application()
