from __future__ import annotations

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Get timezone-aware UTC datetime object."""
    return datetime.now(tz=timezone.utc)
