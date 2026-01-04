from spot2ytm.auth.spotify_authentication_manager import SpotifyAuthenticationManager
from spot2ytm.auth.ytmusic_client_factory import YtMusicAuthenticationManager

from spot2ytm.clients.spotfiy_client import SpotifyClient
from spot2ytm.clients.ytmusic_client import YTMusicClient

from spot2ytm.services.playlist_fetcher import PlaylistFetcher
from spot2ytm.services.track_matcher import TrackMatcher
from spot2ytm.services.playlist_migrator import PlaylistMigrator

def create_app():
    spotify_auth = SpotifyAuthenticationManager()
    spotify_client = SpotifyClient(spotify_auth)

    ytmusic = YtMusicAuthenticationManager().create()
    ytmusic_client = YTMusicClient(ytmusic)

    fetcher = PlaylistFetcher(spotify_client)
    matcher = TrackMatcher(ytmusic_client)

    return PlaylistMigrator(fetcher, matcher, ytmusic_client, spotify_client)
