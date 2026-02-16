"""Application factory and initialization module.

This module provides the main entry point for creating and configuring the application.
It assembles all the necessary components (authentication managers, API clients, and services)
into a complete PlaylistMigrator instance.
"""

from spot2ytm.auth.spotify_authentication_manager import SpotifyAuthenticationManager
from spot2ytm.auth.ytmusic_client_factory import YtMusicAuthenticationManager

from spot2ytm.clients.spotfiy_client import SpotifyClient
from spot2ytm.clients.ytmusic_client import YTMusicClient

from spot2ytm.services.playlist_fetcher import PlaylistFetcher
from spot2ytm.services.track_matcher import TrackMatcher
from spot2ytm.services.playlist_migrator import PlaylistMigrator


def create_app():
    """Create and initialize the application with all necessary components.
    
    This factory function instantiates all required authentication managers, API clients,
    and services, then assembles them into a complete PlaylistMigrator instance that can
    be used to migrate playlists from Spotify to YouTube Music.
    
    Returns:
        PlaylistMigrator: Fully configured playlist migrator instance ready for use.
    """
    spotify_auth = SpotifyAuthenticationManager()
    spotify_client = SpotifyClient(spotify_auth)

    ytmusic = YtMusicAuthenticationManager().create()
    ytmusic_client = YTMusicClient(ytmusic)

    fetcher = PlaylistFetcher(spotify_client)
    matcher = TrackMatcher(ytmusic_client)

    return PlaylistMigrator(fetcher, matcher, ytmusic_client, spotify_client)
