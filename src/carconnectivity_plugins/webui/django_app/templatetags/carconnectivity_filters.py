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
        
        # Add tooltip with timestamps
        if with_tooltip:
            return_str += f'<a href="#" data-toggle="tooltip" title="Last updated {element.last_updated} &#10;Last changed {element.last_changed}" class="js-convert-time-title text-decoration-none text-reset">'
        
        # Format value
        unit = None
        if isinstance(element.value, Enum):
            value = element.value.value
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
        
        if with_tooltip:
            return_str += '</a>'
        
        if linebreak:
            return_str += '<br>'
        
        return mark_safe(return_str)
    
    elif isinstance(element, GenericObject):
        if not element.enabled:
            return ''
        
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
