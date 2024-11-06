from __future__ import annotations

from enum import Enum


class HashingAlgorithm(Enum):
    """Enumeration for hashing algorithms."""

    SHA256 = "sha256"


class SignatureAlgorithm(Enum):
    """Enumeration for signature algorithms."""

    HS256 = "HS256"


class Encoding(Enum):
    """Enumeration for encodings."""

    ASCII = "ascii"
