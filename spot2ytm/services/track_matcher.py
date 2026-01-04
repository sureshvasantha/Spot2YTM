from typing import List
from spot2ytm.clients.ytmusic_client import YTMusicClient
from spot2ytm.domain.track import Track


class TrackMatcher:
    """
    Find songs(videoId) in YTMusic for given songs from spotify 
    """
    def __init__(self, ytmusic: YTMusicClient) -> None:
        self.ytmusic_client = ytmusic

    def match(self, tracks: List[Track]) -> List[str]:
        video_ids = []
        for track in tracks:
            video_id = self.ytmusic_client.search_song(track.title, track.album)
            if video_id:
                video_ids.append(video_id)
        return video_ids
