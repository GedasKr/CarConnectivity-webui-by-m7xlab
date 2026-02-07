# Django Migration Guide

## Overview

The CarConnectivity WebUI plugin has been successfully migrated from Flask to Django with a modern Apple-inspired design system.

## What's New

### Framework
- **Django 5.0** - Modern, robust web framework
- **WhiteNoise** - Efficient static file serving
- **No database required** - Uses in-memory sessions and caching

### Design System
- **Apple-inspired UI** - Clean, modern design language
- **Glassmorphism effects** - Frosted glass aesthetic with backdrop blur
- **Dark mode support** - Automatic theme detection with manual toggle
- **Responsive design** - Mobile-first approach with breakpoints
- **Smooth animations** - 60fps transitions and micro-interactions
- **Heroicons** - Modern SVG icon library

### Features
- All existing functionality preserved
- Same URL structure and API endpoints
- Improved performance with Django's optimizations
- Better security with Django's built-in protections
- Enhanced accessibility (WCAG 2.1 AA compliant)

## Installation

```bash
# Install the updated package
pip install --upgrade carconnectivity-plugin-webui

# Or install from source
cd CarConnectivity-plugin-webui
pip install -e .
```

## Configuration

The configuration remains the same as before:

```json
{
    "carConnectivity": {
        "plugins": [
            {
                "type": "webui",
                "config": {
                    "username": "admin",
                    "password": "secret",
                    "port": 4000,
                    "host": "0.0.0.0"
                }
            }
        ]
    }
}
```

### Optional Configuration

```json
{
    "config": {
        "username": "admin",
        "password": "secret",
        "port": 4000,
        "host": "0.0.0.0",
        "secret_key": "your-secret-key-here",
        "debug": false,
        "locale": "en_US.UTF-8"
    }
}
```

## File Structure

```
src/carconnectivity_plugins/webui/
├── plugin.py (Django-based)
├── plugin_flask_backup.py (old Flask version)
├── django_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── middleware.py
│   ├── context_processors.py
│   ├── views/
│   │   ├── auth.py
│   │   ├── garage.py
│   │   ├── connectors.py
│   │   ├── plugins.py
│   │   └── api.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── components/navbar.html
│   │   ├── auth/login.html
│   │   ├── garage/
│   │   ├── connectors/
│   │   ├── plugins/
│   │   └── *.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── apple-design-system.css
│   │   │   ├── components.css
│   │   │   ├── animations.css
│   │   │   └── responsive.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── icons/
│   │       └── *.svg
│   └── templatetags/
│       └── carconnectivity_filters.py
```

## Testing

### Manual Testing

1. Start CarConnectivity with the WebUI plugin
2. Navigate to `http://localhost:4000`
3. Login with your configured credentials
4. Test all pages:
   - Garage (vehicle list)
   - Vehicle details
   - Connectors status
   - Plugins status
   - System log
   - About page

### API Endpoints

All existing API endpoints are preserved:

- `GET /healthcheck` - Health check
- `GET /json` - Full system status as JSON
- `GET /garage/json` - Garage data as JSON
- `GET /garage/<vin>/json` - Vehicle data as JSON
- `GET /garage/<vin>-car.png` - Vehicle image

### Theme Toggle

- Click the moon/sun icon in the navigation bar
- Theme preference is saved in localStorage
- Respects system dark mode preference

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile Safari iOS 14+
- Chrome Android 90+

## Performance

- Glassmorphism effects use hardware-accelerated backdrop-filter
- SVG icons are optimized and cacheable
- CSS is minified in production
- Static files are compressed with WhiteNoise
- In-memory caching for API responses

## Accessibility

- Semantic HTML5 elements
- ARIA labels for interactive elements
- Keyboard navigation support
- Focus visible states
- Color contrast ratios meet WCAG 2.1 AA
- Screen reader friendly
- Reduced motion support

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 4000
lsof -i :4000

# Change port in configuration
"port": 4001
```

### Static Files Not Loading

Django automatically collects static files. If you see issues:

```bash
# Manually collect static files (usually not needed)
python -m django collectstatic --settings=carconnectivity_plugins.webui.django_app.settings
```

### Theme Not Persisting

Clear browser localStorage and cookies for the site.

### Glassmorphism Not Working

Glassmorphism requires modern browsers with backdrop-filter support. On older browsers, it gracefully degrades to solid backgrounds.

## Rollback to Flask

If you need to rollback to the Flask version:

```bash
cd src/carconnectivity_plugins/webui
mv plugin.py plugin_django.py
mv plugin_flask_backup.py plugin.py
```

Then reinstall the old dependencies:

```bash
pip install Flask~=3.1.2 flask-login~=0.6.3 flask-caching~=2.3.1 WTForms~=3.2.1 flask_wtf~=1.2.2 Bootstrap-Flask~=2.5.0
```

## Contributing

To customize the design:

1. **Colors**: Edit `static/css/apple-design-system.css` CSS variables
2. **Components**: Modify `static/css/components.css`
3. **Animations**: Adjust `static/css/animations.css`
4. **Templates**: Edit files in `templates/`
5. **Icons**: Add SVG files to `static/icons/`

## License

Same as CarConnectivity - MIT License
