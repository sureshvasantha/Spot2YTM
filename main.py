from ytmusicapi import YTMusic, OAuthCredentials
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.environ['YT_CLIENT_ID'] 
client_secret = os.environ['YT_CLIENT_SECRET'] 

ytmusic = YTMusic('oauth.json', oauth_credentials=OAuthCredentials(client_id=client_id, client_secret=client_secret))

