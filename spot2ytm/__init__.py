"""Spot2YTM - Spotify to YouTube Music Playlist Migration Tool.

This package provides an automated solution to migrate playlists from Spotify to YouTube Music.
It handles authentication with both services, fetches tracks from Spotify playlists, matches them
with YouTube Music content, and creates/populates the corresponding YouTube Music playlists.

Main Components:
    - auth: Authentication managers for Spotify and YouTube Music
    - clients: API clients for interacting with Spotify and YouTube Music
    - services: Business logic for fetching, matching, and migrating playlists
    - domain: Data models like Track
    - config: Configuration and logging settings
"""
