from typing import List
from spot2ytm.clients.spotfiy_client import SpotifyClient
from spot2ytm.domain.track import Track

class PlaylistFetcher:
    """
    Fetch Songs from Spotify playlist
    """
    def __init__(self, spotify_client: SpotifyClient) -> None:
        self.spotify_client = spotify_client

    def fetch(self, playlist_id: str) -> List[Track]:
        return self.spotify_client.get_playlist_songs(playlist_id)