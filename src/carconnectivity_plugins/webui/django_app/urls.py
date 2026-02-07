"""URL configuration for CarConnectivity WebUI plugin."""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from carconnectivity_plugins.webui.django_app.views import auth, garage, connectors, plugins, api

urlpatterns = [
    # Root redirects to garage
    path('', garage.root, name='root'),
    
    # Authentication
    path('login', auth.login_view, name='login'),
    path('logout', auth.logout_view, name='logout'),
    
    # Garage (vehicles)
    path('garage/', include([
        path('', garage.garage_view, name='garage'),
        path('json', garage.garage_json, name='garage_json'),
        path('<str:vin>/', garage.vehicle_view, name='vehicle'),
        path('<str:vin>/json', garage.vehicle_json, name='vehicle_json'),
        path('<str:vin>-car.png.json', garage.vehicle_img_json, name='vehicle_img_json'),
        path('<str:vin>-car.png', garage.vehicle_img, name='vehicle_img'),
    ])),
    
    # Connectors
    path('connectors/', include([
        path('status', connectors.status_view, name='connectors_status'),
        path('<str:connector_id>/config', connectors.config_view, name='connector_config'),
        path('<str:connector_id>/log', connectors.log_view, name='connector_log'),
    ])),
    
    # Plugins
    path('plugins/', include([
        path('status', plugins.status_view, name='plugins_status'),
        path('<str:plugin_id>/config', plugins.config_view, name='plugin_config'),
        path('<str:plugin_id>/log', plugins.log_view, name='plugin_log'),
    ])),
    
    # System
    path('log', api.log_view, name='log'),
    path('about', api.about_view, name='about'),
    path('healthcheck', api.healthcheck, name='healthcheck'),
    path('restart', api.restart_view, name='restart'),
    path('restartrefresh', api.restartrefresh_view, name='restartrefresh'),
    path('json', api.json_status, name='json_status'),
]

# Serve static files
if settings.STATICFILES_DIRS:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
