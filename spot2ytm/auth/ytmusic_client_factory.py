from ytmusicapi import YTMusic
from config.settings import settings

class YtMusicAuthenticationManager:
    """
    Creates authenticated YTMusic client instances
    using browser JSON credentials.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(YtMusicAuthenticationManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, credentials_path=settings.YTMUSIC_AUTH_FILE) -> None:
        self.credentials_path = credentials_path

    
    def create(self) -> YTMusic:
        """
        Returns an authenticated YTMusic client.
        """
        return YTMusic(str(self.credentials_path))
    
