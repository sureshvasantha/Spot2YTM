"""Track matching service.

This module provides functionality to match Spotify tracks with their equivalents
in YouTube Music using search and metadata matching.
"""

from typing import List
from spot2ytm.clients.ytmusic_client import YTMusicClient
from spot2ytm.domain.track import Track


class TrackMatcher:
    """Matches Spotify tracks to YouTube Music videos.
    
    Searches for YouTube Music equivalents of Spotify tracks and collects their
    video IDs for playlist population. Currently uses track title for matching,
    with album information available for future enhancements.
    """
    
    def __init__(self, ytmusic: YTMusicClient) -> None:
        """Initialize the track matcher.
        \n        Args:
            ytmusic: YTMusicClient instance for searching songs.
        """
        self.ytmusic_client = ytmusic

    def match(self, tracks: List[Track]) -> List[str]:
        """Match a list of Spotify tracks to YouTube Music video IDs.
        \n        Searches for each track in YouTube Music and collects the video IDs of
        successfully matched songs. Currently searches by track title only.
        \n        Args:
            tracks: List of Track objects from Spotify to match.
            \n        Returns:
            List[str]: List of YouTube Music video IDs for matched tracks.
        """
        video_ids = []
        for track in tracks:
            # video_id = self.ytmusic_client.search_song(track.title, track.album)
            ###  search only with name for now
            video_id = self.ytmusic_client.search_song(track.title)
            if video_id:
                video_ids.append(video_id)
        return video_ids
