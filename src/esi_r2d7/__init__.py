"""Async client for ESI R2D7 RS-232 blind controllers, built on serialx."""

from .protocol import (
    CONNECT_ERRORS,
    MAX_CHANNEL,
    MAX_SYSTEM,
    MIN_CHANNEL,
    MIN_SYSTEM,
    STOP_COALESCE_SECONDS,
    R2D7Connection,
    command,
)

__all__ = [
    "CONNECT_ERRORS",
    "MAX_CHANNEL",
    "MAX_SYSTEM",
    "MIN_CHANNEL",
    "MIN_SYSTEM",
    "STOP_COALESCE_SECONDS",
    "R2D7Connection",
    "command",
]
