"""Connector views for CarConnectivity WebUI."""
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
    """Display connector status."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    return render(request, 'connectors/status.html', {
        'connectors': car_connectivity.connectors
    })


@require_http_methods(["GET"])
def config_view(request: HttpRequest, connector_id: str) -> HttpResponse:
    """Display connector configuration."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    if connector_id not in car_connectivity.connectors.connectors:
        raise Http404(f"Connector {connector_id} not found")
    
    connector = car_connectivity.connectors.connectors[connector_id]
    
    return render(request, 'connectors/config.html', {
        'connector': connector
    })


@require_http_methods(["GET"])
def log_view(request: HttpRequest, connector_id: str) -> HttpResponse:
    """Display connector log."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    if connector_id not in car_connectivity.connectors.connectors:
        raise Http404(f"Connector {connector_id} not found")
    
    connector = car_connectivity.connectors.connectors[connector_id]
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    return render(request, 'connectors/log.html', {
        'connector': connector,
        'formatter': formatter
    })
