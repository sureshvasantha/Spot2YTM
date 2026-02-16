"""Spotify Web API client.

This module provides a client interface for interacting with the Spotify Web API,
including user profile access, playlist management, and track retrieval.
"""

from typing import List
import requests
from spot2ytm.auth.spotify_authentication_manager import SpotifyAuthenticationManager
from spot2ytm.config.settings import settings
from spot2ytm.domain.track import Track


class SpotifyClient:
    """Client for interacting with the Spotify Web API.
    
    Provides methods to fetch user profiles, retrieve playlists, and get track information
    from Spotify using authenticated API requests.
    """
    
    def __init__(self, auth_manager: SpotifyAuthenticationManager):
        """Initialize the Spotify client.
        \n        Args:
            auth_manager: SpotifyAuthenticationManager instance for handling OAuth tokens.
        """
        self.auth_manager = auth_manager

    def _headers(self) -> dict:
        """Generate authorization headers for API requests.
        \n        Returns:
            dict: Dictionary containing the Authorization header with Bearer token.
        """
        return {
            'Authorization': 'Bearer ' +  self.auth_manager.get_token()  # type: ignore
            }
            
    def get_profile(self) -> dict:
        """Retrieve the authenticated user's profile information.
        \n        Returns:
            dict: User profile data including display name, email, and ID.
        """
        response = requests.get(url='https://api.spotify.com/v1/me', headers=self._headers()).json()
        return response
    
    def get_my_playlists(self) -> dict:
        """Retrieve all playlists owned by the authenticated user.
        \n        Returns:
            dict: Paginated list of user's playlists.
        """
        response = requests.get(url='https://api.spotify.com/v1/me/playlists', headers=self._headers()).json()
        return response

    def get_playlist_name_desc(self, playlist_id: str) -> tuple:
        """Retrieve a playlist's name and description.
        \n        Args:
            playlist_id: The Spotify playlist ID.
            \n        Returns:
            tuple: A tuple of (playlist_name, playlist_description).
        """
        params = {
            'fields': 'name,description'
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=self._headers(), params=params).json()
        return response['name'], response['description']

    def get_playlist(self, playlist_id: str) -> dict:
        """Retrieve a playlist with its track information.
        \n        Args:
            playlist_id: The Spotify playlist ID.
            \n        Returns:
            dict: Playlist data including name and tracks with track details.
        """
        params = {
            'fields': 'name,tracks(items(track(name,album(name))))'
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=self._headers(), params=params).json()
        return response

    def get_playlist_songs_count(self, playlist_id: str) -> tuple:
        """Get the total number of songs and limit in a playlist.
        \n        Args:
            playlist_id: The Spotify playlist ID.
            \n        Returns:
            tuple: A tuple of (total_songs, limit).
        """
        params = {
            'fields': 'total,limit'
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=self._headers(), params=params).json()
        return response['total'], response['limit']    

    def get_playlist_songs(self, playlist_id: str) -> List[Track]:
        """Retrieve all songs from a Spotify playlist with pagination.
        \n        Args:
            playlist_id: The Spotify playlist ID.
            \n        Returns:
            List[Track]: List of Track objects containing title and album information.
        """
        params = {
            'fields': 'next,previous,items(track(name,album(name)))',
        }
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        songs = []
        while url:
            response = requests.get(url=url, headers=self._headers(), params=params).json()
            for item in response['items']:
                songs.append(Track(title=item['track']['name'], album=item['track']['album']['name']))
            url = response['next']
        return songs