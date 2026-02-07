"""Authentication views for CarConnectivity WebUI."""
from __future__ import annotations
from typing import TYPE_CHECKING
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from carconnectivity_plugins.webui.django_app import get_users

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@require_http_methods(["GET", "POST"])
@csrf_protect
def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user login.
    
    GET: Display login form
    POST: Process login credentials
    """
    error = None
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me', False)
        
        users = get_users()
        if username in users and users[username] == password:
            # Set session
            request.session['user_id'] = username
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when browser closes
            else:
                request.session.set_expiry(1209600)  # 2 weeks
            
            # Redirect to next page or garage
            next_page = request.GET.get('next', '/')
            return redirect(next_page)
        else:
            error = 'User unknown or password is wrong'
    
    return render(request, 'auth/login.html', {
        'error': error,
        'next': request.GET.get('next', '/')
    })


@require_http_methods(["GET"])
def logout_view(request: HttpRequest) -> HttpResponse:
    """Handle user logout."""
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')
