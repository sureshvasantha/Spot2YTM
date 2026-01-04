
import logging
from spot2ytm.clients.spotfiy_client import SpotifyClient
from spot2ytm.clients.ytmusic_client import YTMusicClient
from spot2ytm.services.playlist_fetcher import PlaylistFetcher
from spot2ytm.services.track_matcher import TrackMatcher

logger = logging.getLogger(__name__)

class PlaylistMigrator:

    def __init__(self, fetcher: PlaylistFetcher, matcher: TrackMatcher, ytmusic: YTMusicClient, spotify: SpotifyClient) -> None:
        self.spotify_client = spotify
        self.ytmusic_client = ytmusic
        self.fetcher = fetcher
        self.matcher = matcher
    
    def migrate(self, spotify_playlist_id: str, ytmusic_playlist_name: str = ""):

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

        # Fetch songs(Track) from spotify playlist
        songs = self.fetcher.fetch(spotify_playlist_id)

        # Search those songs in YTM, get ID
        song_ids = self.matcher.match(songs)

        # Add those IDs to YTM Playlist
        self.ytmusic_client.add_songs_to_playlist(yt_playlist_id, song_ids)

        return yt_playlist_id
