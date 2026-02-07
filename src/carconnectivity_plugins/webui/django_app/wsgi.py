"""WSGI config for CarConnectivity WebUI plugin."""
import os

# Don't call get_wsgi_application() at module import time
# It will be called by plugin.py after Django is configured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carconnectivity_plugins.webui.django_app.settings')

# Application will be set by plugin.py
application = None

def get_application():
    """Get or create the WSGI application."""
    global application
    if application is None:
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
    return application
