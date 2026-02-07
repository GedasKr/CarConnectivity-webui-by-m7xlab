# QuickStart Guide - Django WebUI

## Installation

### Option 1: Install from PyPI (when published)

```bash
pip install --upgrade carconnectivity-plugin-webui
```

### Option 2: Install from Source

```bash
cd CarConnectivity-plugin-webui
pip install -e .
```

## Configuration

Create or update your `carConnectivity.json`:

```json
{
    "carConnectivity": {
        "log_level": "info",
        "connectors": [
            {
                "type": "your-connector-type",
                "config": {
                    "username": "your-username",
                    "password": "your-password"
                }
            }
        ],
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

## Running

```bash
# Start CarConnectivity with your config
carconnectivity --config carConnectivity.json

# Or if running from source
python -m carconnectivity --config carConnectivity.json
```

## Accessing the UI

1. Open your browser
2. Navigate to: `http://localhost:4000`
3. Login with your configured credentials (admin/secret)
4. Enjoy the modern UI!

## Features to Try

### Theme Toggle
- Click the moon/sun icon in the top navigation
- Theme preference is saved automatically

### Vehicle Management
- View all vehicles in the garage
- Click on a vehicle to see detailed information
- View vehicle location on map (if available)
- Check battery level, range, and other stats

### System Monitoring
- View connector status
- View plugin status
- Check system logs
- View version information

### API Access
- JSON endpoints available at:
  - `/json` - Full system status
  - `/garage/json` - All vehicles
  - `/garage/<vin>/json` - Specific vehicle
  - `/healthcheck` - Health status

## Troubleshooting

### Port Already in Use

```bash
# Change port in config
"port": 4001
```

### Can't Login

- Check username and password in config
- Clear browser cookies and try again

### Static Files Not Loading

```bash
# Reinstall the package
pip install --force-reinstall carconnectivity-plugin-webui
```

### Theme Not Working

- Clear browser localStorage
- Refresh the page
- Try a different browser

## Browser Requirements

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers supported

## Getting Help

- Check `DJANGO_MIGRATION.md` for detailed information
- Check `IMPLEMENTATION_SUMMARY.md` for technical details
- Report issues on GitHub

## Advanced Configuration

### Custom Secret Key

```json
{
    "config": {
        "username": "admin",
        "password": "secret",
        "port": 4000,
        "secret_key": "your-long-random-secret-key-here"
    }
}
```

### Debug Mode (Development Only)

```json
{
    "config": {
        "username": "admin",
        "password": "secret",
        "port": 4000,
        "debug": true
    }
}
```

### Custom Locale

```json
{
    "config": {
        "username": "admin",
        "password": "secret",
        "port": 4000,
        "locale": "en_US.UTF-8"
    }
}
```

## Next Steps

- Explore all the pages
- Try dark mode
- Test on mobile device
- Check out the API endpoints
- Customize the design (see DJANGO_MIGRATION.md)

Enjoy your modern CarConnectivity WebUI! 🚗✨
