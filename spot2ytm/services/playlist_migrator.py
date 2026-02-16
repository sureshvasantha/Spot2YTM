"""Playlist migration service.

This module orchestrates the complete workflow for migrating playlists from Spotify
to YouTube Music, including fetching songs, matching them, and creating playlists.
"""

import logging
from spot2ytm.clients.spotfiy_client import SpotifyClient
from spot2ytm.clients.ytmusic_client import YTMusicClient
from spot2ytm.services.playlist_fetcher import PlaylistFetcher
from spot2ytm.services.track_matcher import TrackMatcher

logger = logging.getLogger(__name__)


class PlaylistMigrator:
    """Orchestrates the migration of playlists from Spotify to YouTube Music.
    
    Coordinates the complete migration workflow including fetching playlists from Spotify,
    matching tracks to YouTube Music equivalents, creating playlists in YouTube Music,
    and populating them with the matched songs.
    """

    def __init__(self, fetcher: PlaylistFetcher, matcher: TrackMatcher, ytmusic_client: YTMusicClient, spotify_client: SpotifyClient) -> None:
        """Initialize the playlist migrator with required components.
        \n        Args:
            fetcher: PlaylistFetcher instance for fetching Spotify playlists.
            matcher: TrackMatcher instance for finding YouTube Music equivalents.
            ytmusic_client: YTMusicClient instance for YouTube Music operations.
            spotify_client: SpotifyClient instance for Spotify operations.
        """
        self.spotify_client = spotify_client
        self.ytmusic_client = ytmusic_client
        self.fetcher = fetcher
        self.matcher = matcher
    
    def migrate(self, spotify_playlist_id: str, ytmusic_playlist_name: str = "") -> str | None:
        """Migrate a Spotify playlist to YouTube Music.
        \n        Fetches all songs from a Spotify playlist, searches for equivalent songs in
        YouTube Music, creates a new YouTube Music playlist with the same metadata,
        and populates it with the matched songs.
        \n        Args:
            spotify_playlist_id: The ID of the Spotify playlist to migrate.
            ytmusic_playlist_name: Optional custom name for the YouTube Music playlist.
                                   If not provided, uses the original Spotify playlist name.
            \n        Returns:
            str | None: The YouTube Music playlist ID if migration succeeded, None otherwise.
        """

        #  create playlist in YTM
        pl_name, pl_desc = self.spotify_client.get_playlist_name_desc(spotify_playlist_id)
        
        if ytmusic_playlist_name:
            pl_name = ytmusic_playlist_name

        yt_playlist_id = self.ytmusic_client.get_or_create_playlist(pl_name, pl_desc)

        if not yt_playlist_id:
            logger.error(
                "Migration aborted: failed to create or fetch YT Music playlist. "
                "spotify_playlist_id=%s name=%s",
                spotify_playlist_id,
                pl_name
            )
            return
        
        logger.info("YTMusic Playlist created. ID: %s, Name: %s", yt_playlist_id, pl_name)

        # Fetch songs(Track) from spotify playlist
        songs = self.fetcher.fetch(spotify_playlist_id)

        logger.info("All song names are fetched from spotify playlist")

        # Search those songs in YTM, get ID
        song_ids = self.matcher.match(songs)
        logger.info("Songs are searched in YTM and collected YTM song IDs")

        # Add those IDs to YTM Playlist
        self.ytmusic_client.add_songs_to_playlist(yt_playlist_id, song_ids)
        logger.info("Songs are added to playlist")

        return yt_playlist_id
