from dataclasses import dataclass

@dataclass(frozen=True)
class Track:
    title: str
    album: str