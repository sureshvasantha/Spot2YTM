from ytmusicapi import YTMusic
import json
from ytmusicapi import YTMusic
from dotenv import load_dotenv
from spot2ytm.config.settings import settings

load_dotenv()


def setup(authenticate=False):
    if authenticate:
        ytmusic = YTMusic(str(settings.YTMUSIC_AUTH_FILE))
    else:
        ytmusic = YTMusic()
    return ytmusic

def main():
    ytmusic = setup(True)
    search_results = ytmusic.search(query="Karuthavenlam Galeejam from Velaikaran", filter="songs")
    # print("Length of results: ", len(search_results))
    song_video_id = search_results[0]['videoId']
    print("Song Video ID: ", song_video_id)
    # print(json.dumps(search_results[:10]))
    
    songs_to_add = [song_video_id]
    # watch_playlist = ytmusic.get_watch_playlist(videoId=song_video_id, limit=10)['tracks']
    # songs_to_add += [watch_playlist[i]['videoId'] for i in range(len(watch_playlist))]
    # print(songs_to_add)
    # print(json.dumps(search_results, indent=2))
    # my_playlists = ytmusic.get_library_playlists()
    # pl = json.loads(json.dumps(my_playlists))
    # for i in pl:
    #     print(i)
    # print(ytmusic.create_playlist(title="Test Playlist", description="For demo purposes.", video_ids=['R_VeibrODpg']))
    print(ytmusic.add_playlist_items(playlistId='PLov11V84qSmhZtv35dPqNOepHzjd5b7ax', videoIds=songs_to_add))

main()