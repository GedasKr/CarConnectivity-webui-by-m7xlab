"""Garage views for CarConnectivity WebUI."""
from __future__ import annotations
from typing import TYPE_CHECKING
import io
import json
from base64 import b64encode
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from carconnectivity_plugins.webui.django_app import get_car_connectivity

if TYPE_CHECKING:
    from django.http import HttpRequest

# Check if PIL is available
SUPPORT_IMAGES = False
try:
    from PIL import Image  # noqa: F401
    SUPPORT_IMAGES = True
except ImportError:
    pass


@require_http_methods(["GET"])
def root(request: HttpRequest) -> HttpResponse:
    """Redirect root to garage."""
    return redirect('garage')


@require_http_methods(["GET"])
def garage_view(request: HttpRequest) -> HttpResponse:
    """Display garage with all vehicles."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    return render(request, 'garage/garage.html', {
        'garage': car_connectivity.garage
    })


@require_http_methods(["GET"])
@cache_page(5)
def garage_json(request: HttpRequest) -> JsonResponse:
    """Return garage data as JSON."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity or not car_connectivity.garage:
        raise Http404("Garage not found")
    
    pretty = request.GET.get('pretty', 'false').lower() == 'true'
    in_locale = request.GET.get('in_locale', 'false').lower() == 'true'
    with_locale = request.GET.get('with_locale', None)
    
    if with_locale:
        locale_str = with_locale
    elif in_locale and car_connectivity.connectors and 'webui' in car_connectivity.connectors.connectors:
        locale_str = car_connectivity.connectors.connectors['webui'].active_config.get('locale')
    else:
        locale_str = None
    
    vehicle_json_str = car_connectivity.garage.as_json(pretty=pretty, in_locale=locale_str)
    
    response = HttpResponse(vehicle_json_str, content_type='application/json')
    response['Cache-Control'] = 'private, max-age=5'
    return response


@require_http_methods(["GET"])
def vehicle_view(request: HttpRequest, vin: str) -> HttpResponse:
    """Display vehicle details."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    vehicle = car_connectivity.garage.get_vehicle(vin)
    if not vehicle:
        raise Http404(f"Vehicle with VIN {vin} not found")
    
    return render(request, 'garage/vehicle.html', {
        'vehicle': vehicle
    })


@require_http_methods(["GET"])
@cache_page(5)
def vehicle_json(request: HttpRequest, vin: str) -> HttpResponse:
    """Return vehicle data as JSON."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    vehicle = car_connectivity.garage.get_vehicle(vin)
    if not vehicle:
        raise Http404(f"Vehicle with VIN {vin} not found")
    
    pretty = request.GET.get('pretty', 'false').lower() == 'true'
    in_locale = request.GET.get('in_locale', 'false').lower() == 'true'
    with_locale = request.GET.get('with_locale', None)
    
    if with_locale:
        locale_str = with_locale
    elif in_locale and car_connectivity.connectors and 'webui' in car_connectivity.connectors.connectors:
        locale_str = car_connectivity.connectors.connectors['webui'].active_config.get('locale')
    else:
        locale_str = None
    
    vehicle_json_str = vehicle.as_json(pretty=pretty, in_locale=locale_str)
    
    response = HttpResponse(vehicle_json_str, content_type='application/json')
    response['Cache-Control'] = 'private, max-age=5'
    return response


@require_http_methods(["GET"])
def vehicle_img(request: HttpRequest, vin: str) -> HttpResponse:
    """Return vehicle image."""
    car_connectivity = get_car_connectivity()
    if not car_connectivity:
        raise Http404("CarConnectivity instance not connected")
    
    vehicle = car_connectivity.garage.get_vehicle(vin)
    if not vehicle:
        fallback = request.GET.get('fallback')
        if fallback:
            return redirect(f'/static/{fallback}')
        raise Http404(f"Vehicle with VIN {vin} not found")
    
    if not SUPPORT_IMAGES:
        fallback = request.GET.get('fallback')
        if fallback:
            return redirect(f'/static/{fallback}')
        raise Http404("PIL module not available, cannot serve vehicle images")
    
    # Check if vehicle has car picture
    if ('car_picture' not in vehicle.images.images or 
        not vehicle.images.images['car_picture'].enabled or 
        vehicle.images.images['car_picture'].value is None):
        fallback = request.GET.get('fallback')
        if fallback:
            return redirect(f'/static/{fallback}')
        raise Http404(f"Vehicle with VIN {vin} has no car picture")
    
    # Serve image
    img_io = io.BytesIO()
    vehicle.images.images['car_picture'].value.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Check if JSON format requested
    if request.path.endswith('.json'):
        json_map = {
            'type': 'image/png',
            'encoding': 'base64',
            'data': b64encode(img_io.read()).decode()
        }
        return JsonResponse(json_map)
    
    return FileResponse(img_io, content_type='image/png')
