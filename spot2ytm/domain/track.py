"""Domain model for music tracks.

This module defines the Track data class representing a music track with essential metadata.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    """Represents a music track with immutable metadata.
    
    This is a frozen dataclass that represents a track from a music streaming service.
    The immutable nature ensures track data cannot be accidentally modified.
    
    Attributes:
        title: The name/title of the track.
        album: The album name the track belongs to.
    """
    
    title: str
    album: str