import requests
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_BASE_URL = "https://accounts.spotify.com/" 
TOKEN_URL = "https://accounts.spotify.com/api/token"

def request_access_token():
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(url=TOKEN_URL, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=data).json()
    return response['access_token'], response['expires_in']