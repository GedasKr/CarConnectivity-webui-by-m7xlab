"""Custom template filters for CarConnectivity elements."""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from enum import Enum
from decimal import Decimal
from datetime import timedelta
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from carconnectivity.attributes import GenericAttribute, FloatAttribute
from carconnectivity.objects import GenericObject

if TYPE_CHECKING:
    pass

register = template.Library()


@register.filter
def format_cc_element(element, alt_title: Optional[str] = None, with_tooltip: bool = True, linebreak: bool = False) -> str:
    """
    Format CarConnectivity element for display.
    
    Args:
        element: GenericAttribute or GenericObject to format
        alt_title: Alternative title to display
        with_tooltip: Whether to include tooltip with timestamps
        linebreak: Whether to add line break at end
    
    Returns:
        Formatted HTML string
    """
    if isinstance(element, GenericAttribute):
        if not element.enabled:
            return ''
        
        return_str = ''
        
        # Add title
        if alt_title is not None:
            return_str += escape(alt_title)
        else:
            return_str += escape(element.name)
        
        if len(return_str) > 0:
            return_str += ': '
        
        # Remove tooltip - we show last update near title instead
        # if with_tooltip:
        #     return_str += f'<a href="#" data-toggle="tooltip" title="Last updated {element.last_updated} &#10;Last changed {element.last_changed}" class="js-convert-time-title text-decoration-none text-reset">'
        
        # Format value
        unit = None
        if isinstance(element.value, Enum):
            # Clean enum values - remove class prefix
            value = str(element.value.value)
            if '.' in value:
                value = value.split('.')[-1]
            value = value.replace('_', ' ').title()
        elif isinstance(element, FloatAttribute):
            value, unit = element.in_locale(locale=None)
            if value is not None and element.precision is not None:
                precision_digits = 0
                precision_tmp = element.precision
                while precision_tmp < 1:
                    precision_digits += 1
                    precision_tmp *= 10
                value = round(value, precision_digits)
                value = f'{value:.{precision_digits}f}'
            elif value is not None:
                value = f'{Decimal(value):n}'
        else:
            value, unit = element.in_locale(locale=None)
        
        return_str += escape(str(value))
        if unit is not None:
            return_str += escape(str(unit))
        
        # if with_tooltip:
        #     return_str += '</a>'
        
        if linebreak:
            return_str += '<br>'
        
        return mark_safe(return_str)
    
    elif isinstance(element, GenericObject):
        if not element.enabled:
            return ''
        
        # Special handling for capabilities - display as badges
        if element.id == 'capabilities' or 'capabilities' in str(type(element)).lower():
            badges = []
            for child in element.children:
                if child.enabled:
                    child_id = escape(child.id).replace('_', ' ').title()
                    status_class = 'badge-success' if 'status' in str(child).lower() and 'true' in str(child).lower() else 'badge-primary'
                    badges.append(f'<span class="badge {status_class}" style="margin: 2px; display: inline-block;">{child_id}</span>')
            return mark_safe('<div style="display: flex; flex-wrap: wrap; gap: 4px;">' + ''.join(badges) + '</div>')
        
        # Special handling for nested objects (drives, charging, position_location, etc)
        if len(element.children) > 0 and any(hasattr(child, 'value') for child in element.children):
            items = []
            for child in element.children:
                if child.enabled and hasattr(child, 'value'):
                    key = escape(child.id).replace('_', ' ').title()
                    
                    # Format value
                    if isinstance(child.value, Enum):
                        value = str(child.value.value)
                        if '.' in value:
                            value = value.split('.')[-1]
                        value = escape(value.replace('_', ' ').title())
                    elif isinstance(child.value, float):
                        # Round floats to 1 decimal place
                        value = f'{child.value:.1f}'
                    else:
                        value = escape(str(child.value))
                    
                    unit = ''
                    if hasattr(child, 'unit') and child.unit:
                        unit = escape(str(child.unit))
                    items.append(f'<div style="margin-bottom: 8px;"><span style="color: var(--color-text-secondary); font-size: var(--font-size-sm);">{key}:</span> <span style="color: var(--color-text-primary); font-weight: var(--font-weight-medium);">{value}{unit}</span></div>')
            if items:
                return mark_safe('<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: var(--space-sm);">' + ''.join(items) + '</div>')
        
        # Default handling for other objects
        return_str = ''
        for child in element.children:
            if child.enabled:
                return_str += format_cc_element(child, child.id, with_tooltip, linebreak)
        
        if linebreak:
            return_str += '<br>'
        
        return mark_safe(return_str)
    
    return str(element)


@register.filter
def ansi2html(ansi_str: str) -> str:
    """
    Convert ANSI color codes to HTML.
    
    Args:
        ansi_str: String with ANSI color codes
    
    Returns:
        HTML string with color spans
    """
    ansi_str = escape(ansi_str)
    
    # Standard colors
    ansi_str = ansi_str.replace('\033[30m', '<span style="color:black;">')
    ansi_str = ansi_str.replace('\033[31m', '<span style="color:red;">')
    ansi_str = ansi_str.replace('\033[32m', '<span style="color:green;">')
    ansi_str = ansi_str.replace('\033[33m', '<span style="color:yellow;">')
    ansi_str = ansi_str.replace('\033[34m', '<span style="color:blue;">')
    ansi_str = ansi_str.replace('\033[35m', '<span style="color:magenta;">')
    ansi_str = ansi_str.replace('\033[36m', '<span style="color:cyan;">')
    ansi_str = ansi_str.replace('\033[37m', '<span style="color:white;">')
    
    # Bright colors
    ansi_str = ansi_str.replace('\033[90m', '<span style="color:black;">')
    ansi_str = ansi_str.replace('\033[91m', '<span style="color:red;">')
    ansi_str = ansi_str.replace('\033[92m', '<span style="color:green;">')
    ansi_str = ansi_str.replace('\033[93m', '<span style="color:yellow;">')
    ansi_str = ansi_str.replace('\033[94m', '<span style="color:blue;">')
    ansi_str = ansi_str.replace('\033[95m', '<span style="color:magenta;">')
    ansi_str = ansi_str.replace('\033[96m', '<span style="color:cyan;">')
    ansi_str = ansi_str.replace('\033[97m', '<span style="color:white;">')
    
    # Reset
    ansi_str = ansi_str.replace('\033[0m', '</span>')
    
    return mark_safe(ansi_str)


@register.simple_tag
def timedelta_filter(seconds: int) -> timedelta:
    """
    Convert seconds to timedelta.
    
    Args:
        seconds: Number of seconds
    
    Returns:
        timedelta object
    """
    return timedelta(seconds=seconds)


@register.filter
def format_log_record(record, formatter) -> str:
    """
    Format log record using formatter.
    
    Args:
        record: Log record
        formatter: Logging formatter
    
    Returns:
        Formatted log string
    """
    return formatter.format(record)


@register.filter
def mask_sensitive(config_dict) -> str:
    """
    Mask sensitive data in configuration dictionary and render as beautiful JSON.
    
    Args:
        config_dict: Configuration dictionary
    
    Returns:
        HTML with syntax-highlighted JSON and masked sensitive fields
    """
    import json
    import re
    
    if not isinstance(config_dict, dict):
        config_str = str(config_dict)
    else:
        config_str = json.dumps(config_dict, indent=2, default=str)
    
    # Mask password fields
    sensitive_keys = ['password', 'passwd', 'pwd', 'secret', 'token', 'api_key', 'apikey']
    
    for key in sensitive_keys:
        # Match patterns like: "password": "value" or 'password': 'value'
        pattern = rf'''(['"]){key}\1\s*:\s*(['"])([^'"]+)\2'''
        config_str = re.sub(pattern, rf'\1{key}\1: \2********\2', config_str, flags=re.IGNORECASE)
    
    # Syntax highlighting
    config_str = escape(config_str)
    
    # Highlight keys (blue)
    config_str = re.sub(r'"([^"]+)"(\s*:)', r'<span style="color: #0066cc; font-weight: 500;">"\1"</span>\2', config_str)
    
    # Highlight strings (green)
    config_str = re.sub(r':\s*"([^"]*)"', r': <span style="color: #00aa00;">"\1"</span>', config_str)
    
    # Highlight numbers (orange)
    config_str = re.sub(r':\s*(\d+\.?\d*)', r': <span style="color: #ff8800;">\1</span>', config_str)
    
    # Highlight booleans (purple)
    config_str = re.sub(r'\b(true|false|null)\b', r'<span style="color: #aa00aa;">\1</span>', config_str)
    
    # Highlight masked passwords (red)
    config_str = config_str.replace('********', '<span style="color: #ff0000; font-weight: bold;">********</span>')
    
    return mark_safe(f'<pre style="background: var(--color-surface-elevated); padding: var(--space-lg); border-radius: var(--border-radius-md); overflow-x: auto; line-height: 1.6; font-family: \'SF Mono\', Monaco, \'Courier New\', monospace; font-size: 14px;">{config_str}</pre>')
