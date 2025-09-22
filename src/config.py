import yaml
import os
import logging
from typing import Dict, Any, Optional

# Set up logging for the configuration module
logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Manages the loading and access of all application configuration settings.
    It reads from platforms.yaml and settings.yml.
    """
    
    _instance: Optional['ConfigManager'] = None
    _settings: Dict[str, Any] = {}
    _platforms: Dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        """Ensures a single instance (singleton) of the ConfigManager."""
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_configs()
        return cls._instance

    def _load_configs(self):
        """Loads configuration from YAML files."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_dir = os.path.join(base_dir, 'config')

        settings_path = os.path.join(config_dir, 'settings.yml')
        platforms_path = os.path.join(config_dir, 'platforms.yaml')

        try:
            with open(settings_path, 'r') as f:
                self._settings = yaml.safe_load(f)
            logger.info("✅ Successfully loaded settings from settings.yml")
        except FileNotFoundError:
            logger.error(f"❌ Error: 'settings.yml' not found at {settings_path}")
        except yaml.YAMLError as e:
            logger.error(f"❌ Error parsing 'settings.yml': {e}")
        
        try:
            with open(platforms_path, 'r') as f:
                self._platforms = yaml.safe_load(f)
            logger.info("✅ Successfully loaded platforms from platforms.yaml")
        except FileNotFoundError:
            logger.error(f"❌ Error: 'platforms.yaml' not found at {platforms_path}")
        except yaml.YAMLError as e:
            logger.error(f"❌ Error parsing 'platforms.yaml': {e}")

    def get_setting(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieves a setting by key, with an optional default value."""
        keys = key.split('.')
        value = self._settings
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                logger.warning(f"Setting '{key}' not found. Using default value: {default}")
                return default
        return value

    def get_platforms(self) -> Dict[str, Any]:
        """Returns the dictionary of all platforms."""
        return self._platforms

    def get_platform_details(self, site_name: str) -> Optional[Dict[str, Any]]:
        """Returns details for a specific platform."""
        return self._platforms.get(site_name)

