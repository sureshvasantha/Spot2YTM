"""Playlist fetching service.

This module provides functionality to fetch songs from Spotify playlists.
"""

from typing import List
from spot2ytm.clients.spotfiy_client import SpotifyClient
from spot2ytm.domain.track import Track


class PlaylistFetcher:
    """Fetches songs from Spotify playlists.
    
    Provides a service layer for retrieving track information from Spotify playlists,
    abstracting the Spotify client API.
    """
    
    def __init__(self, spotify_client: SpotifyClient) -> None:
        """Initialize the playlist fetcher.
        \n        Args:
            spotify_client: SpotifyClient instance for API interactions.
        """
        self.spotify_client = spotify_client

    def fetch(self, playlist_id: str) -> List[Track]:
        """Fetch all songs from a Spotify playlist.
        \n        Args:
            playlist_id: The ID of the Spotify playlist to fetch songs from.
            \n        Returns:
            List[Track]: List of Track objects from the playlist.
        """
        return self.spotify_client.get_playlist_songs(playlist_id)