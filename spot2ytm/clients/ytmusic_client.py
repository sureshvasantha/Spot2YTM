"""YouTube Music API client.

This module provides a client interface for interacting with YouTube Music,
including playlist management, song searching, and track addition.
"""

import logging
from ytmusicapi import YTMusic
from typing import List
import json

logger = logging.getLogger(__name__)


class YTMusicClient:
    """Client for interacting with YouTube Music.
    
    Provides methods to search for songs, create and manage playlists,
    and add tracks to YouTube Music playlists.
    """
    
    def __init__(self, ytmusic: YTMusic) -> None:
        """Initialize the YouTube Music client.
        \n        Args:
            ytmusic: An authenticated YTMusic instance.
        """
        self.client = ytmusic

    def get_all_user_playlists(self) -> list:
        """Retrieve all playlists from the user's YouTube Music library.
        \n        Returns:
            list: List of playlist objects with metadata.
        """
        response = self.client.get_library_playlists()
        playlists = json.loads(json.dumps(response))
        return playlists
    
    def get_playlist_by_name(self, name: str) -> dict | None:
        """Find a playlist by its name in the user's library.
        \n        Args:
            name: The name of the playlist to search for.
            \n        Returns:
            dict | None: The playlist object if found, None otherwise.
        """
        playlists = self.get_all_user_playlists()
        for playlist in playlists:
            if playlist['title'] == name:
                return playlist
        return None

    def search_song(self, name: str, album: str = "", artist: str = "") -> str:
        """Search for a song on YouTube Music.
        \n        Constructs a search query from song name and album information,
        then returns the video ID of the first matching song.
        \n        Args:
            name: The name/title of the song to search for.
            album: Optional album name to improve search accuracy.
            artist: Currently unused parameter (kept for API compatibility).
            \n        Returns:
            str: The YouTube Music video ID of the song.
        """
        if not album:
            query = name  
        elif "from" in name.lower():
            query = name  
        else: 
            query = f"{name} from {album}"
        results = self.client.search(query=query, filter="songs")
        return results[0]['videoId']

    def get_or_create_playlist(self, name: str, description: str, video_ids: List[str] = []) -> str:
        """Get an existing playlist by name or create a new one.
        \n        If a playlist with the given name exists in the user's library, returns its ID.
        Otherwise, creates a new playlist with the specified name and description,
        optionally adding initial songs.
        \n        Args:
            name: The name of the playlist.
            description: The description for the playlist.
            video_ids: Optional list of YouTube Music video IDs to add to the new playlist.
            \n        Returns:
            str: The playlist ID, or empty string if creation failed.
        """
        playlist = self.get_playlist_by_name(name)

        if playlist:
            return playlist.get('playlistId', "")
        
        response = self.client.create_playlist(title=name, description=description, video_ids=video_ids)
        
        if isinstance(response, str):
            return response

        if isinstance(response, dict):
            logger.error(
                "YTMusic playlist creation failed. name=%s error=%s",
                name,
                response
            )    
            return ""
        
        # Defensive fallback
        logger.error(
            "Unexpected response type from YTMusic.create_playlist: %s (%r)",
            type(response),
            response
        )
        return ""

    def add_songs_to_playlist(self, playlist_id: str, song_ids: List[str]) -> bool:
        """Add songs to a YouTube Music playlist.
        \n        Args:
            playlist_id: The ID of the target playlist.
            song_ids: List of YouTube Music video IDs to add.
            \n        Returns:
            bool: True if songs were added successfully, False otherwise.
        """
        response = self.client.add_playlist_items(playlistId=playlist_id, videoIds=song_ids, duplicates=True)
        if "succeed" in response['status'].lower(): # type: ignore
            return True
        else:
            logger.warning("Error response from YTMusic while adding song to playlist.\n %s",  response) # type: ignore
            return False