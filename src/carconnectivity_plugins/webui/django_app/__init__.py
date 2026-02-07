"""Django application for CarConnectivity WebUI plugin."""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Optional
    from carconnectivity.carconnectivity import CarConnectivity

# Global configuration storage
_plugin_config: Dict = {}
_car_connectivity: Optional[CarConnectivity] = None
_users: Dict[str, str] = {}


def configure_from_plugin(config: Dict, car_connectivity: CarConnectivity, users: Dict[str, str]) -> None:
    """
    Configure Django application from plugin configuration.
    
    Args:
        config: Plugin configuration dictionary
        car_connectivity: CarConnectivity instance
        users: Dictionary of username -> password
    """
    global _plugin_config, _car_connectivity, _users
    _plugin_config = config
    _car_connectivity = car_connectivity
    _users = users


def get_plugin_config() -> Dict:
    """Get plugin configuration."""
    return _plugin_config


def get_car_connectivity() -> Optional[CarConnectivity]:
    """Get CarConnectivity instance."""
    return _car_connectivity


def get_users() -> Dict[str, str]:
    """Get users dictionary."""
    return _users
