"""Custom authentication middleware for CarConnectivity WebUI."""
from __future__ import annotations
from typing import TYPE_CHECKING
import base64
from django.http import HttpResponseRedirect
from django.urls import reverse
from carconnectivity_plugins.webui.django_app import get_users

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class User:
    """Simple user object for authentication."""
    
    def __init__(self, username: str):
        self.username = username
        self.is_authenticated = True
    
    def get_id(self) -> str:
        return self.username


class CarConnectivityAuthMiddleware:
    """
    Custom authentication middleware for CarConnectivity.
    
    Supports both session-based and HTTP Basic authentication.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = ['/login', '/healthcheck', '/static/']
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Check if path is public
        is_public = any(request.path.startswith(path) for path in self.public_paths)
        
        # Try to authenticate user
        user = None
        
        # Check session first
        if 'user_id' in request.session:
            username = request.session['user_id']
            users = get_users()
            if username in users:
                user = User(username)
        
        # Try HTTP Basic Auth if no session
        if not user:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Basic '):
                try:
                    auth_decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
                    username, password = auth_decoded.split(':', 1)
                    users = get_users()
                    if username in users and users[username] == password:
                        user = User(username)
                except (ValueError, UnicodeDecodeError):
                    pass
        
        # Attach user to request
        request.user = user
        
        # Redirect to login if not authenticated and not public path
        if not user and not is_public:
            return HttpResponseRedirect(reverse('login') + f'?next={request.path}')
        
        response = self.get_response(request)
        return response
