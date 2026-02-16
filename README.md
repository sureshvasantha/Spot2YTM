# Spot2YTM - Spotify Playlist To YT Music Playlist

The main focus of this project is to automate playlist migration from end to end.
None of the features should require more user efforts.

Features:
---

1. Fetches songs (name, album) from Spotify playlist (given ID)
2. Searches the song in YT music search and gets top result song ID (videoId)
3. Creates Playlist in YT Music Library. User Given Name or Name & Desc from given spotify playlist.
4. Adds searched songs in the playlist

TODO:
---

- [ ] Get Spotify playlists of logged in User instead of passing IDs manually.
- [ ] Develop CLI tool (args type and TUI style) 
- [x] Remove prints in `app.py` and log correctly. 
- [ ] Make use of Redis or ACID DB to persist songs IDs to resume addition of songs regardless of app restarts.
- [ ] Handle Rate limiting for searching in YTM.
- [ ] Apply Search Result limit for searching in YTM.
- [ ] Log extensively
- [ ] Handle Exceptions using Custom.
- [ ] Develop proper custom auth for this tool - for Spotify (OAUTH) and YT browser based or Oauth -> end result `browser.json`.



  > Ultimate Goal: 
  > 
  > *Make it generic for all Users.*