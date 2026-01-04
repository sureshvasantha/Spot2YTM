import requests
import os
import json
import time
from spot2ytm.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class SpotifyAuthenticationManager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpotifyAuthenticationManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
    def __init__(self, token_file=settings.SPOTIFY_TOKEN_FILE):
        self.token_file = token_file
        self.token = None
        self.expiry = 0
        self._load_token()

    def _load_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as file:
                data = json.load(file)
                self.token = data.get("token")
                self.expiry = data.get("expiry")
    
    def _save_token(self):
        with open(self.token_file, 'w') as file:
            json.dump({
                "token": self.token,
                "expiry": self.expiry
            }, file)
    
    def _get_current_time(self):
        return int(time.time())
    
    def _is_token_expired(self):
        return self._get_current_time() >= self.expiry
    
    def _request_new_token(self) -> str | Exception:

        data = {
            'grant_type': 'client_credentials',
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET
        }

        response = requests.post(url=settings.SPOTIFY_TOKEN_URL, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=data)
        if response.status_code == 200:
            payload = response.json()
            new_token = payload.get("access_token")
            self.token = new_token
            self.expiry = self._get_current_time() +  payload.get("expires_in")
            self._save_token()
            return new_token
        else:
            return Exception(f"Failed to fetch token: {response.text}")
        
    def get_token(self):
        if self.token is None or self._is_token_expired():
            return self._request_new_token()
        return self.token