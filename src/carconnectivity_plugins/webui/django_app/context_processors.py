"""Context processors for CarConnectivity WebUI."""
from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any
from django.urls import reverse
from carconnectivity_plugins.webui.django_app import get_car_connectivity

if TYPE_CHECKING:
    from django.http import HttpRequest


def navbar(request: HttpRequest) -> Dict[str, Any]:
    """
    Build navigation bar structure.
    
    Returns:
        Dictionary with navbar structure
    """
    car_connectivity = get_car_connectivity()
    
    plugins_sublinks = []
    connectors_sublinks = []
    
    # Build connectors navigation
    if car_connectivity and car_connectivity.connectors and car_connectivity.connectors.enabled:
        connectors_sublinks.append({
            "text": "Status",
            "url": reverse('connectors_status')
        })
        connectors_sublinks.append({"divider": True})
        
        for connector in car_connectivity.connectors.connectors.values():
            connectors_sublinks.append({
                "text": connector.id,
                "url": reverse('connector_config', args=[connector.id])
            })
    
    # Build plugins navigation
    if car_connectivity and car_connectivity.plugins and car_connectivity.plugins.enabled:
        plugins_sublinks.append({
            "text": "Status",
            "url": reverse('plugins_status')
        })
        plugins_sublinks.append({"divider": True})
        
        for plugin in car_connectivity.plugins.plugins.values():
            plugins_sublinks.append({
                "text": plugin.id,
                "url": reverse('plugin_config', args=[plugin.id])
            })
    
    # Build main navigation
    nav = [
        {"text": "Garage", "url": reverse('garage')},
        {
            "text": "Connectors",
            "sublinks": connectors_sublinks,
            "url": reverse('connectors_status')
        },
        {
            "text": "Plugins",
            "sublinks": plugins_sublinks,
            "url": reverse('plugins_status')
        },
        {"text": "Log", "url": reverse('log')},
        {"text": "Grafana", "url": "/grafana/"},
    ]
    
    return {'navbar': nav}


def car_connectivity(request: HttpRequest) -> Dict[str, Any]:
    """
    Provide CarConnectivity instance to templates.
    
    Returns:
        Dictionary with car_connectivity instance
    """
    return {
        'car_connectivity': get_car_connectivity(),
        'current_user': request.user if hasattr(request, 'user') else None,
    }
