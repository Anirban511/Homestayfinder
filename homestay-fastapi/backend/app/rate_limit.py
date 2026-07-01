"""Tiny in-memory fixed-window rate limiter used as a FastAPI dependency.

Mirrors the rate limiting in the scalp-diagnostics project: keyed by client IP,
it allows N requests per window and raises 429 when exceeded. In production this
would be backed by Redis instead of a process-local dict.
"""
import time
from collections import defaultdict

from fastapi import HTTPException, Request, status

from app.config import settings

_hits: dict[str, list[float]] = defaultdict(list)


def rate_limiter(request: Request) -> None:
    client = request.client.host if request.client else "unknown"
    now = time.time()
    window = settings.RATE_LIMIT_WINDOW_SECONDS
    # Drop timestamps older than the window.
    _hits[client] = [t for t in _hits[client] if now - t < window]
    if len(_hits[client]) >= settings.RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded, slow down",
        )
    _hits[client].append(now)
