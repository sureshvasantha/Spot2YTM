"""Application configuration management.

This module defines and manages all configuration settings for the Spot2YTM application,
including API credentials, file paths, and behavior flags. It loads environment variables
and provides a centralized Settings object for use throughout the application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Settings:
    """Central configuration object for the Spot2YTM application.
    
    This class manages all application settings including:
    - Project and data directory paths
    - Spotify API credentials and endpoints
    - YouTube Music authentication file paths
    - Playlist IDs for testing/default playlists
    - Debug and encoding settings
    
    Settings are loaded from environment variables and cached for efficient access.
    """

    def __init__(self):
        """Initialize Settings by loading environment variables and configuring paths."""
        self._load_env()

        # Project paths
        self.BASE_DIR = Path(__file__).resolve().parents[2]
        
        self.DATA_DIR = self.BASE_DIR / "spot2ytm" / "data"

        self.CREDS_DIR = self.BASE_DIR / "spot2ytm" / "creds"

        # Spotify
        self.SPOTIFY_CLIENT_ID = self._get_env("SPOTIFY_CLIENT_ID")
        self.SPOTIFY_CLIENT_SECRET = self._get_env("SPOTIFY_CLIENT_SECRET")
        self.SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
        self.SPOTIFY_API_BASE = "https://api.spotify.com/v1"

        # Auth / Token management
        self.SPOTIFY_TOKEN_FILE = self.CREDS_DIR / "spotify_token.json"
        self.SPOTIFY_TOKEN_EXPIRY_BUFFER = 30  # seconds
        self.YTMUSIC_AUTH_FILE = self.CREDS_DIR / "ytm_browser.json"

        self.GYM_PL_ID = "1R7k82T5vm2pOBcmVPVVbT"
        self.GOVT_BUS_PL_ID = "3xn31tfE0XR0s2FNc9kiB4"
        self.MY_PL_ID = "29dpWoYLHwYyCQba9G1gTH"
        self.MASS_BGM_PL_ID = "5B8YspLAD1fxY5SAwwLy3X"

        # App behavior
        self.DEBUG = self._get_bool("DEBUG", default=False)

        self.DEFAULT_ENCODING = "utf-8"


    # ---------- internal helpers ----------

    def _load_env(self):
        """Load environment variables from .env file."""
        load_dotenv()

    def _get_env(self, key: str, default=None) -> str:
        """Retrieve an environment variable with optional default value.
        \n        Args:
            key: The environment variable name to retrieve.
            default: Optional default value if key is not found.
            \n        Returns:
            str: The environment variable value or default.
            \n        Raises:
            RuntimeError: If the key is not found and no default is provided.
        """
        value = os.getenv(key, default)
        if value is None:
            raise RuntimeError(f"Missing required env var: {key}")
        return value

    def _get_bool(self, key: str, default=False) -> bool:
        """Retrieve an environment variable as a boolean value.
        \n        Args:
            key: The environment variable name to retrieve.
            default: Default boolean value if key is not found.
            \n        Returns:
            bool: True if the value is '1', 'true', or 'yes' (case-insensitive).
        """
        return os.getenv(key, str(default)).lower() in ("1", "true", "yes")


# Singleton-style settings object
settings = Settings()
