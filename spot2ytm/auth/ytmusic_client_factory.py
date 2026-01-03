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
    
    def __init__(self, credentials_path) -> None:
        self.credentials_path = credentials_path

    
    def create(self, authenticate=False) -> YTMusic:
        """
        Returns an authenticated YTMusic client.
        """
        if authenticate:
            ytmusic = YTMusic(str(settings.YTMUSIC_AUTH_FILE))
        else:
            ytmusic = YTMusic()
        return ytmusic
    
