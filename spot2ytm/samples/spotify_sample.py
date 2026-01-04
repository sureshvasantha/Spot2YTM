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

def get_profile():
    response = requests.get(url='https://api.spotify.com/v1/me', headers=header).json()
    print(response)
    return response


def get_playlist(playlist_id):
    params = {
        'fields': 'name,tracks(items(track(name,album(name))))'
    }
    response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=header, params=params).json()
    print(response)
    return response

def get_playlist_songs_count(playlist_id):
    params = {
        'fields': 'total,limit'
    }
    response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=header, params=params).json()
    print(response)
    return response    

def get_playlist_name_desc(playlist_id):
        params = {
            'fields': 'name,description'
        }
        response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=header, params=params).json()
        print(__name__, response)
        return response['name'], response['description']

def get_playlist_songs(playlist_id: str) -> List[Track]:
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
    # get_playlist_songs(MY_PL_ID)
    get_playlist_name_desc(MY_PL_ID)