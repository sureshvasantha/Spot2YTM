from auth.spotify_auth import request_access_token
import requests
import json

SPOTIFY_ACCESS_TOKEN = request_access_token()[0]

header = {
    'Authorization': 'Bearer ' + SPOTIFY_ACCESS_TOKEN
}

GYM_PL_ID = "1R7k82T5vm2pOBcmVPVVbT"
GOVT_BUS_PL_ID = "3xn31tfE0XR0s2FNc9kiB4"
MY_PL_ID = "29dpWoYLHwYyCQba9G1gTH"
MASS_BGM_PL_ID = "5B8YspLAD1fxY5SAwwLy3X" 

def get_profile():
    response = requests.get(url='https://api.spotify.com/v1/me/playlists', headers=header).json()
    print(response)
    return response


def get_playlist(playlist_id):
    params = {
        'fields': 'name,tracks(items(track(name,album(name))))'
    }
    response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=header, params=params).json()
    print(response)
    return response

def get_playlist_items_count(playlist_id):
    params = {
        'fields': 'total,limit'
    }
    response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=header, params=params).json()
    print(response)
    return response    

def get_playlist_items(playlist_id):
    params = {
        'fields': 'items(track(name,album(name)))',
    }
    response = requests.get(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=header, params=params).json()
    print(len(response['items']))
    print(response)
    return response

if __name__ == '__main__':
    get_playlist_items_count(GYM_PL_ID)
    get_playlist_items(GYM_PL_ID)