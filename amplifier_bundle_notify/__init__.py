"""Amplifier Notify Bundle.

Desktop notifications when assistant turns complete.
"""

from pathlib import Path


def get_bundle_path() -> Path:
    """Return the path to the bundle directory."""
    return Path(__file__).parent.parent
