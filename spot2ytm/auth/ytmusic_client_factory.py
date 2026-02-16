"""YouTube Music authentication manager.

This module manages authentication with YouTube Music using stored browser credentials.
It provides a factory for creating authenticated YTMusic client instances.
"""

from ytmusicapi import YTMusic
from spot2ytm.config.settings import settings


class YtMusicAuthenticationManager:
    """Creates authenticated YouTube Music client instances.
    
    This class implements a singleton pattern to manage authentication with YouTube Music
    using stored browser JSON credentials. It provides a factory method to create
    authenticated YTMusic client instances.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern for authentication manager.
        \n        Ensures only one instance of YtMusicAuthenticationManager exists throughout
        the application's lifetime.
        """
        if not cls._instance:
            cls._instance = super(YtMusicAuthenticationManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, credentials_path=settings.YTMUSIC_AUTH_FILE) -> None:
        """Initialize the YouTube Music authentication manager.
        \n        Args:
            credentials_path: Path to the browser JSON credentials file.
                            Defaults to settings.YTMUSIC_AUTH_FILE.
        """
        self.credentials_path = credentials_path

    
    def create(self) -> YTMusic:
        """Create and return an authenticated YTMusic client.
        \n        Uses the stored browser credentials to authenticate with YouTube Music.
        \n        Returns:
            YTMusic: An authenticated YouTube Music client instance.
        """
        return YTMusic(str(self.credentials_path))
    
