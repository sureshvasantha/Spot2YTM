"""Spotify OAuth 2.0 authentication manager.

This module handles OAuth 2.0 authentication with Spotify's API, including token
requests, caching, expiration checking, and credential persistence.
"""

import requests
import os
import json
import time
from spot2ytm.config.settings import settings
from spot2ytm.auth.exceptions import SpotifyAuthenticationError
import logging

logger = logging.getLogger(__name__)


class SpotifyAuthenticationManager:
    """Manages Spotify OAuth 2.0 authentication and token lifecycle.
    
    Implements a singleton pattern to ensure only one authentication manager instance exists.
    Handles token acquisition, caching, expiration tracking, and automatic renewal.
    Uses the Client Credentials OAuth 2.0 flow for server-to-server authentication.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Implement singleton pattern for authentication manager.
        \n        Ensures only one instance of SpotifyAuthenticationManager exists throughout
        the application's lifetime.
        """
        if not cls._instance:
            cls._instance = super(SpotifyAuthenticationManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
        
    def __init__(self, token_file=settings.SPOTIFY_TOKEN_FILE):
        """Initialize the authentication manager.
        \n        Args:
            token_file: Path to the file where tokens are cached. Defaults to settings.SPOTIFY_TOKEN_FILE.
        """
        self.token_file = token_file
        self.token = None
        self.expiry = 0
        self._load_token()

    def _load_token(self):
        """Load a cached token and expiry time from the token file.
        \n        If the token file exists, reads and loads the stored token and expiry timestamp.
        """
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as file:
                data = json.load(file)
                self.token = data.get("token")
                self.expiry = data.get("expiry")
    
    def _save_token(self):
        """Save the current token and expiry time to the token file.
        \n        Persists the token to disk so it can be reused across application restarts
        without requiring new authentication requests.
        """
        with open(self.token_file, 'w') as file:
            json.dump({
                "token": self.token,
                "expiry": self.expiry
            }, file)
    
    def _get_current_time(self) -> int:
        """Get the current Unix timestamp.
        \n        Returns:
            int: Current time as a Unix timestamp (seconds since epoch).
        """
        return int(time.time())
    
    def _is_token_expired(self) -> bool:
        """Check if the current token has expired.
        \n        Returns:
            bool: True if the token has expired, False otherwise.
        """
        return self._get_current_time() >= self.expiry
    
    def _request_new_token(self) -> str:
        """Request a new access token from Spotify's token endpoint.
        
        Uses the Client Credentials OAuth 2.0 flow with credentials from settings
        to obtain a new access token. Saves the new token and expiry time locally.
        
        Returns:
            str: The new access token if successful.
        
        Raises:
            SpotifyAuthenticationError: If the token request fails due to invalid
                credentials, network issues, or API errors.
        """
        data = {
            'grant_type': 'client_credentials',
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET
        }

        try:
            response = requests.post(
                url=settings.SPOTIFY_TOKEN_URL,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data=data
            )
            response.raise_for_status()  # Raise exception for bad status codes
            
            payload = response.json()
            new_token = payload.get("access_token")
            
            if not new_token:
                logger.error("Token response missing 'access_token' field")
                raise SpotifyAuthenticationError(
                    "Spotify API returned an invalid response: missing access token"
                )
            
            self.token = new_token
            self.expiry = self._get_current_time() + payload.get("expires_in", 3600)
            self._save_token()
            logger.info("Successfully obtained new Spotify access token")
            return new_token
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"Spotify API returned error {response.status_code}: {response.text}"
            logger.error(error_msg)
            raise SpotifyAuthenticationError(error_msg) from e
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to connect to Spotify token endpoint: {str(e)}"
            logger.error(error_msg)
            raise SpotifyAuthenticationError(error_msg) from e
            
        except (ValueError, KeyError) as e:
            error_msg = f"Invalid response format from Spotify: {str(e)}"
            logger.error(error_msg)
            raise SpotifyAuthenticationError(error_msg) from e
        
    def get_token(self) -> str:
        """Get a valid Spotify access token.
        
        Returns a cached token if available and not expired. Otherwise, requests and
        caches a new token before returning it.
        
        Returns:
            str: A valid Spotify OAuth 2.0 access token.
        
        Raises:
            SpotifyAuthenticationError: If token acquisition fails. This can occur due to:
                - Invalid or missing Spotify API credentials
                - Network connectivity issues
                - Spotify API server errors
        """
        if self.token is None or self._is_token_expired():
            return self._request_new_token()
        return self.token