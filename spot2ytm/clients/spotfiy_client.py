from typing import List
import requests
from spot2ytm.auth.spotify_authentication_manager import SpotifyAuthenticationManager
from spot2ytm.config.settings import settings
from spot2ytm.domain.track import Track


class SpotifyClient:
    def __init__(self, auth_manager: SpotifyAuthenticationManager):
        self.auth_manager = auth_manager

    def _headers(self):
        return {
            'Authorization': 'Bearer ' +  self.auth_manager.get_token()  # type: ignore
            }
            
    def get_profile(self):
        response = requests.get(url='https://api.spotify.com/v1/me', headers=self._headers()).json()
        return response
    
    def get_my_playlists(self):
        response = requests.get(url='https://api.spotify.com/v1/me/playlists', headers=self._headers()).json()
        return response

    def get_playlist_name_desc(self, playlist_id):
        params = {
            'fields': 'name,description'
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=self._headers(), params=params).json()
        return response['name'], response['description']

    def get_playlist(self, playlist_id):
        params = {
            'fields': 'name,tracks(items(track(name,album(name))))'
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=self._headers(), params=params).json()
        return response

    def get_playlist_songs_count(self, playlist_id):
        params = {
            'fields': 'total,limit'
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=self._headers(), params=params).json()
        return response['total'], response['limit']    

    def get_playlist_songs(self, playlist_id: str) -> List[Track]:
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