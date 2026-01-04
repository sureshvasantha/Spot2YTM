import logging
from ytmusicapi import YTMusic
from typing import List
import json

logger = logging.getLogger(__name__)

class YTMusicClient:
    def __init__(self, ytmusic: YTMusic) -> None:
        self.client = ytmusic

    def get_all_user_playlists(self):
        response = self.client.get_library_playlists()
        playlists = json.loads(json.dumps(response))
        return playlists
    
    def get_playlist_by_name(self, name: str):
        playlists = self.get_all_user_playlists()
        for playlist in playlists:
            if playlist['title'] == name:
                return playlist
        return None

    def search_song(self, name: str, album: str, artist: str):
        if "from" in name.lower():
            query = name  
        else: 
            query = f"{name} from {album}"

        results = self.client.search(query=query, filter="songs")
        return results[0]['videoId']

    def create_playlist(self, name: str, description: str):
        playlist = self.get_playlist_by_name(name)
        if playlist:
            response = playlist['playlistId']
        else:
            response = self.client.create_playlist(title=name, description=description)
        return response

    def add_songs_to_playlist(self, playlist_id: str, song_ids: List[str]):
        response = self.client.add_playlist_items(playlistId=playlist_id, videoIds=song_ids)
        if "succeed" in response['status'].lower(): # type: ignore
            return True
        else:
            logger.warning("Error response from YTMusic while adding song to playlist.\n %s",  response['status']) # type: ignore
            return False