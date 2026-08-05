"""ShineMonitor REST API client.

Two thin I/O shells over a shared sansio core:
- `ShineMonitorAPI` (this module) — synchronous, uses httpx.Client.
- `shinemonitor_api.aio.AsyncShineMonitorAPI` — async, uses httpx.AsyncClient.
"""

from __future__ import annotations

from ._client_sync import ShineMonitorAPI
from ._protocol import (
    KNOWN_APPS,
    AppProfile,
    AuthState,
    ShineMonitorAuthError,
    ShineMonitorError,
)
from .models import (
    DeviceIdentifier,
    LastData,
    LastDataGrid,
    LastDataMain,
    LastDataPV,
    LastDataSystem,
    parse_last_data,
)

__version__ = "0.8.1"

__all__ = [
    "KNOWN_APPS",
    "AppProfile",
    "AuthState",
    "DeviceIdentifier",
    "LastData",
    "LastDataGrid",
    "LastDataMain",
    "LastDataPV",
    "LastDataSystem",
    "ShineMonitorAPI",
    "ShineMonitorAuthError",
    "ShineMonitorError",
    "parse_last_data",
]
