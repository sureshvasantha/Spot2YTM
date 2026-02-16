"""Custom exceptions for Spotify authentication.

This module defines exception classes specific to Spotify authentication failures.
"""


class SpotifyAuthenticationError(Exception):
    """Raised when Spotify authentication fails.
    
    This exception is raised when any step of the Spotify OAuth 2.0 authentication
    process fails, including:
    - Invalid or missing API credentials
    - Network connectivity issues
    - Spotify API server errors
    - Invalid response format from Spotify
    """
    pass

