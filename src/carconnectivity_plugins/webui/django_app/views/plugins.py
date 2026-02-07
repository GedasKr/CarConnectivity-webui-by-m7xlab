"""Plugin views for CarConnectivity WebUI."""
from __future__ import annotations
from typing import TYPE_CHECKING
import logging
from django.shortcuts import render
from django.http import Http404
from django.views.decorators.http import require_http_methods
from carconnectivity_plugins.webui.django_app import get_car_connectivity

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET"])
def status_view(request: HttpRequest) -> HttpResponse:
    """Display plugin status."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    return render(request, 'plugins/status.html', {
        'plugins': car_connectivity.plugins
    })


@require_http_methods(["GET"])
def config_view(request: HttpRequest, plugin_id: str) -> HttpResponse:
    """Display plugin configuration."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    if plugin_id not in car_connectivity.plugins.plugins:
        raise Http404(f"Plugin {plugin_id} not found")
    
    plugin = car_connectivity.plugins.plugins[plugin_id]
    
    return render(request, 'plugins/config.html', {
        'plugin': plugin
    })


@require_http_methods(["GET"])
def log_view(request: HttpRequest, plugin_id: str) -> HttpResponse:
    """Display plugin log."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    if plugin_id not in car_connectivity.plugins.plugins:
        raise Http404(f"Plugin {plugin_id} not found")
    
    plugin = car_connectivity.plugins.plugins[plugin_id]
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    return render(request, 'plugins/log.html', {
        'plugin': plugin,
        'formatter': formatter
    })
