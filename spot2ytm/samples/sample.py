"""Sample utility module for debugging and path investigation.

This module demonstrates basic path resolution functionality for the Spot2YTM project.
"""

from pathlib import Path

print(Path(__file__).resolve())
print(Path(__file__).resolve().parents[2])