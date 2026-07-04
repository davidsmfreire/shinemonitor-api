"""Constants for the ShineMonitor integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "shinemonitor"
MANUFACTURER = "ShineMonitor"

UPDATE_INTERVAL = timedelta(seconds=60)

CONF_APP_PROFILE = "app_profile"
DEFAULT_APP_PROFILE = "watchpower"
