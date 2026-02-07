"""Module implements the plugin to provide a Django-based web UI."""
from __future__ import annotations
from typing import TYPE_CHECKING
import logging
import threading
import os
import locale
from wsgiref.simple_server import make_server, WSGIServer

from carconnectivity.errors import ConfigurationError
from carconnectivity.util import config_remove_credentials
from carconnectivity_plugins.base.plugin import BasePlugin

if TYPE_CHECKING:
    from typing import Dict, Optional
    from carconnectivity.carconnectivity import CarConnectivity

# Check for PIL support
SUPPORT_IMAGES: bool = False
SUPPORT_IMAGES_STR: str = ""
try:
    import PIL  # noqa: F401
    SUPPORT_IMAGES = True
except ImportError as exc:
    if str(exc) == "No module named 'PIL'":
        SUPPORT_IMAGES_STR = str(exc) + " (cannot find pillow library)"
    else:
        SUPPORT_IMAGES_STR = str(exc)

LOG: logging.Logger = logging.getLogger("carconnectivity.plugins.webui")


class Plugin(BasePlugin):
    """
    Django-based WebUI Plugin for CarConnectivity.
    
    Args:
        car_connectivity (CarConnectivity): An instance of CarConnectivity.
        config (Dict): Configuration dictionary containing connection details.
    """
    
    def __init__(self, plugin_id: str, car_connectivity: CarConnectivity, config: Dict, *args, 
                 initialization: Optional[Dict] = None, **kwargs) -> None:
        BasePlugin.__init__(self, plugin_id=plugin_id, car_connectivity=car_connectivity, 
                          config=config, log=LOG, *args, initialization=initialization, **kwargs)
        
        self.webthread: Optional[threading.Thread] = None
        self.server: Optional[WSGIServer] = None
        
        # Configure host and port
        if 'host' not in config or not config['host']:
            self.active_config['host'] = '0.0.0.0'  # nosec
        else:
            self.active_config['host'] = config['host']
        
        if 'port' in config and config['port'] is not None:
            self.active_config['port'] = config['port']
            if not self.active_config['port'] or self.active_config['port'] < 1 or self.active_config['port'] > 65535:
                raise ConfigurationError('Invalid port specified in config ("port" out of range, must be 1-65535)')
        else:
            self.active_config['port'] = 4000
        
        # Configure users
        users: Dict[str, str] = {}
        if 'username' in config and config['username'] is not None \
                and 'password' in config and config['password'] is not None:
            users[config['username']] = config['password']
        
        if 'users' in config and config['users'] is not None:
            for user in config['users']:
                if 'username' in user and 'password' in user:
                    users[user['username']] = user['password']
        
        self.active_config['passwords'] = users
        
        # Configure locale
        if 'locale' in config and config['locale'] is not None:
            self.active_config['locale'] = config['locale']
            try:
                locale.setlocale(locale.LC_ALL, self.active_config['locale'])
            except locale.Error as err:
                LOG.warning('Invalid locale specified in config ("locale" must be a valid locale): %s', err)
        elif 'locale' in car_connectivity.active_config and car_connectivity.active_config['locale'] is not None:
            self.active_config['locale'] = car_connectivity.active_config['locale']
        else:
            self.active_config['locale'] = locale.getlocale()[0]
        
        # Configure Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carconnectivity_plugins.webui.django_app.settings')
        
        # Set Django secret key from config
        if 'secret_key' in config and config['secret_key']:
            os.environ['DJANGO_SECRET_KEY'] = config['secret_key']
        
        # Set debug mode
        if 'debug' in config and config['debug']:
            os.environ['DJANGO_DEBUG'] = 'True'
        
        # Pass configuration to Django app
        from carconnectivity_plugins.webui.django_app import configure_from_plugin
        configure_from_plugin(config, car_connectivity, users)
        
        # Get WSGI application
        from carconnectivity_plugins.webui.django_app.wsgi import application
        self.application = application
        
        # Create WSGI server
        self.server = make_server(
            self.active_config['host'],
            self.active_config['port'],
            self.application,
            server_class=WSGIServer
        )
        
        LOG.info("Loading Django WebUI plugin with config %s", config_remove_credentials(config))
    
    def startup(self) -> None:
        """Start the Django WSGI server."""
        LOG.info("Starting Django WebUI plugin on %s:%s", 
                self.active_config['host'], self.active_config['port'])
        
        self.webthread = threading.Thread(target=self.server.serve_forever)
        self.webthread.name = 'carconnectivity.plugins.webui-webthread'
        self.webthread.daemon = True
        self.webthread.start()
        
        self.healthy._set_value(value=True)  # pylint: disable=protected-access
        LOG.debug("Django WebUI plugin started successfully")
    
    def shutdown(self) -> None:
        """Shutdown the Django WSGI server."""
        if self.server is not None:
            LOG.info("Shutting down Django WebUI plugin")
            self.server.shutdown()
        
        if self.webthread is not None and self.webthread.is_alive():
            self.webthread.join(timeout=5)
        
        return super().shutdown()
    
    def get_version(self) -> str:
        """Get plugin version."""
        try:
            from carconnectivity_plugins.webui._version import __version__
            return __version__
        except ImportError:
            return "unknown"
    
    def get_features(self) -> dict[str, tuple[bool, str]]:
        """Get plugin features."""
        features: dict[str, tuple[bool, str]] = {}
        features['Images'] = (SUPPORT_IMAGES, SUPPORT_IMAGES_STR)
        features['Django'] = (True, "Django 5.0+")
        return features
    
    def get_type(self) -> str:
        """Get plugin type."""
        return "carconnectivity-plugin-webui"
    
    def get_name(self) -> str:
        """Get plugin name."""
        return "WebUI Plugin (Django)"
