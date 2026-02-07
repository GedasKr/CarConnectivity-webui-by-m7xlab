"""API and system views for CarConnectivity WebUI."""
from __future__ import annotations
from typing import TYPE_CHECKING
import sys
import os
import time
import threading
import logging
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from carconnectivity_plugins.webui.django_app import get_car_connectivity

if TYPE_CHECKING:
    from django.http import HttpRequest


@require_http_methods(["GET"])
def healthcheck(request: HttpRequest) -> HttpResponse:
    """Health check endpoint."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        return HttpResponse('unhealthy', status=500)
    
    if car_connectivity.is_healthy():
        return HttpResponse('ok')
    return HttpResponse('unhealthy', status=503)


@require_http_methods(["GET"])
def log_view(request: HttpRequest) -> HttpResponse:
    """Display system log."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    return render(request, 'log.html', {
        'car_connectivity': car_connectivity,
        'formatter': formatter
    })


@require_http_methods(["GET"])
def about_view(request: HttpRequest) -> HttpResponse:
    """Display about page with version information."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    versions = {}
    if car_connectivity.version and car_connectivity.version.enabled and car_connectivity.version.value:
        versions['CarConnectivity'] = car_connectivity.version.value
    
    if car_connectivity.connectors and car_connectivity.connectors.enabled:
        for connector in car_connectivity.connectors.connectors.values():
            versions[connector.id] = connector.get_version()
    
    if car_connectivity.plugins and car_connectivity.plugins.enabled:
        for plugin in car_connectivity.plugins.plugins.values():
            versions[plugin.id] = plugin.get_version()
    
    return render(request, 'about.html', {
        'versions': versions
    })


@require_http_methods(["GET"])
def restart_view(request: HttpRequest) -> HttpResponse:
    """Restart the application."""
    def delayed_restart():
        time.sleep(10)
        python = sys.executable
        os.execl(python, python, *sys.argv)  # nosec
    
    t = threading.Thread(target=delayed_restart)
    t.start()
    
    return render(request, 'restart.html')


@require_http_methods(["GET"])
def restartrefresh_view(request: HttpRequest) -> HttpResponse:
    """Display restart refresh page."""
    return render(request, 'restart.html')


@require_http_methods(["GET"])
@cache_page(5)
def json_status(request: HttpRequest) -> HttpResponse:
    """Return full CarConnectivity status as JSON."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    pretty = request.GET.get('pretty', 'false').lower() == 'true'
    in_locale = request.GET.get('in_locale', 'false').lower() == 'true'
    with_locale = request.GET.get('with_locale', None)
    
    if with_locale:
        locale_str = with_locale
    elif in_locale and car_connectivity.connectors and 'webui' in car_connectivity.connectors.connectors:
        locale_str = car_connectivity.connectors.connectors['webui'].active_config.get('locale')
    else:
        locale_str = None
    
    json_str = car_connectivity.as_json(pretty=pretty, in_locale=locale_str)
    
    response = HttpResponse(json_str, content_type='application/json')
    response['Cache-Control'] = 'private, max-age=5'
    return response
