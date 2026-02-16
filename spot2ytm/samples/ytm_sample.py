"""YouTube Music API sample implementation and testing.

This module demonstrates various YouTube Music API operations including playlist
creation, song searching, and track addition. Intended for development and testing purposes.
"""

from ytmusicapi import YTMusic
import json
from dotenv import load_dotenv
from spot2ytm.clients.ytmusic_client import YTMusicClient
from spot2ytm.config.settings import settings

load_dotenv()


def setup(authenticate: bool = False) -> YTMusic:
    """Initialize and return a YouTube Music client.
    \n    Args:
        authenticate: If True, authenticates using stored credentials.
                     If False, returns an unauthenticated client.
                     \n    Returns:
        YTMusic: An initialized YTMusic client instance.
    """
    if authenticate:
        ytmusic = YTMusic(str(settings.YTMUSIC_AUTH_FILE))
    else:
        ytmusic = YTMusic()
    return ytmusic

def main():
    """Main sample function demonstrating YouTube Music operations.
    \n    Searches for a song and adds it to a playlist.
    """
    ytmusic = setup(True)
    ytm_client = YTMusicClient(ytmusic)

    search_results = ytmusic.search(query="Thalapathy Kacheri", filter="songs")
    # print("Length of results: ", len(search_results))
    song_video_id = search_results[0]['videoId']
    print("Song Video ID: ", song_video_id)
    # print(json.dumps(search_results[:10]))
    
    # songs_to_add = [song_video_id]
    # watch_playlist = ytmusic.get_watch_playlist(videoId=song_video_id, limit=10)['tracks']
    # songs_to_add += [watch_playlist[i]['videoId'] for i in range(len(watch_playlist))]
    # print(songs_to_add)
    # print(json.dumps(search_results, indent=2))
    # my_playlists = ytmusic.get_library_playlists()
    # pl = json.loads(json.dumps(my_playlists))
    # for i in pl:
    #     print(i)
    # print(ytmusic.create_playlist(title="Test Playlist", description="For demo purposes.", video_ids=['R_VeibrODpg']))
    print(ytmusic.add_playlist_items(playlistId='PLov11V84qSmhZtv35dPqNOepHzjd5b7ax', videoIds=['R_VeibrODpg', song_video_id], duplicates=True))
    # print(ytm_client.get_or_create_playlist("Test Playlist 2", "Test 2")) 

main()