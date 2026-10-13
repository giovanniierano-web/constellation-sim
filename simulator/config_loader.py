import json
import os

class ConfigLoader:
    """Loads basic simulation parameters from config.json."""
    
    DEFAULT_CONFIG_PATH = "config.json"

    @classmethod
    def load_config(cls, filepath: str = DEFAULT_CONFIG_PATH) -> dict:
        default_settings = {
            "satellite_limit": 5,
            "stations": ["Station_North", "Station_South"]
        }
        
        if not os.path.exists(filepath):
            return default_settings
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                default_settings.update(user_config)
                return default_settings
        except Exception:
            return default_settings