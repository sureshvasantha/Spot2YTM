"""Spotify API sample implementation and testing.

This module demonstrates various Spotify API operations including user profiles,
playlist retrieval, and track fetching. Intended for development and testing purposes.
"""

from typing import List
from spot2ytm.auth.spotify_authentication_manager import SpotifyAuthenticationManager
import requests
import json
from spot2ytm.domain.track import Track
from spot2ytm.config.settings import settings

spotify_auth = SpotifyAuthenticationManager()
SPOTIFY_ACCESS_TOKEN = spotify_auth.get_token()

header = {
    'Authorization': 'Bearer ' + SPOTIFY_ACCESS_TOKEN # pyright: ignore[reportOperatorIssue]
}

GYM_PL_ID = "1R7k82T5vm2pOBcmVPVVbT"
GOVT_BUS_PL_ID = "3xn31tfE0XR0s2FNc9kiB4"
MY_PL_ID = "29dpWoYLHwYyCQba9G1gTH"
MASS_BGM_PL_ID = "5B8YspLAD1fxY5SAwwLy3X" 


def get_profile() -> dict:
    """Retrieve and print the authenticated user's Spotify profile.
    \n    Returns:
        dict: User profile data from Spotify.
    """
    response = requests.get(url='https://api.spotify.com/v1/me', headers=header).json()
    print(response)
    return response


def get_playlist(playlist_id: str) -> dict:
    """Fetch and print a playlist with its tracks.
    \n    Args:
        playlist_id: The Spotify playlist ID.
        \n    Returns:
        dict: Playlist data including name and tracks.
    """
    params = {
        'fields': 'name,tracks(items(track(name,album(name))))'
    }
    response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=header, params=params).json()
    print(response)
    return response

def get_playlist_songs_count(playlist_id: str) -> dict:
    """Get the total song count and pagination limit for a playlist.
    \n    Args:
        playlist_id: The Spotify playlist ID.
        \n    Returns:
        dict: Response data with 'total' and 'limit' fields.
    """
    params = {
        'fields': 'total,limit'
    }
    response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=header, params=params).json()
    print(response)
    return response    

def get_playlist_name_desc(playlist_id: str) -> tuple:
    """Fetch and return a playlist's name and description.
    \n    Args:
        playlist_id: The Spotify playlist ID.
        \n    Returns:
        tuple: A tuple of (playlist_name, playlist_description).
    """
    params = {
        'fields': 'name,description'
    }
    response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=header, params=params).json()
    print(__name__, response)
    return response['name'], response['description']

def get_playlist_songs(playlist_id: str) -> List[Track]:
    """Fetch all songs from a Spotify playlist with pagination.
    \n    Args:
        playlist_id: The Spotify playlist ID.
        \n    Returns:
        List[Track]: List of Track objects from the playlist.
    """
        params = {
            'fields': 'next,previous,items(track(name,album(name)))',
        }
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        songs = []
        while url:
            response = requests.get(url=url, headers=header, params=params).json()
            for item in response['items']:
                songs.append(Track(title=item['track']['name'], album=item['track']['album']['name']))
            url = response['next']

        # with open(file=settings.DATA_DIR / "songs.txt", mode='w+', encoding=settings.DEFAULT_ENCODING) as fp:
        #     for track in songs:
        #         fp.write(f"{track.title} FROM {track.album}\n")
        return songs

if __name__ == '__main__':
    get_playlist_songs_count(MY_PL_ID)
    get_playlist_songs_count(GOVT_BUS_PL_ID)
    # get_playlist_songs(MY_PL_ID)
    # get_playlist_name_desc(MY_PL_ID)
    get_playlist_songs_count(MASS_BGM_PL_ID)