import requests
from spot2ytm.auth.spotify_authentication_manager import SpotifyAuthenticationManager


class Spotify:
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


    def get_playlist(self, playlist_id):
        params = {
            'fields': 'name,tracks(items(track(name,album(name))))'
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=self._headers(), params=params).json()
        print(response)
        return response

    def get_playlist_items_count(self, playlist_id):
        params = {
            'fields': 'total,limit'
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=self._headers(), params=params).json()
        print(response)
        return response    

    def get_playlist_items(self, playlist_id):
        params = {
            'fields': 'items(track(name,album(name)))',
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=self._headers(), params=params).json()
        print(len(response['items']))
        print(response)
        return response