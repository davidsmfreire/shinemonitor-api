"""DataUpdateCoordinator for ShineMonitor."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from shinemonitor_api import ShineMonitorAuthError
from shinemonitor_api.aio import AsyncShineMonitorAPI
from shinemonitor_api.models import DeviceIdentifier, LastData

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.httpx_client import get_async_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


class ShineMonitorCoordinator(DataUpdateCoordinator[dict[str, LastData]]):
    """Coordinator that polls last-data for every inverter on the account."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        username: str,
        password: str,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=UPDATE_INTERVAL,
        )
        self._username = username
        self._password = password
        self._api = AsyncShineMonitorAPI(client=get_async_client(hass))
        self._logged_in = False
        self.devices: list[DeviceIdentifier] = []

    async def _async_setup(self) -> None:
        """One-time login and device enumeration."""
        await self._login_and_list_devices()

    async def _login_and_list_devices(self) -> None:
        try:
            await self._api.login(self._username, self._password)
        except ShineMonitorAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        self._logged_in = True
        self.devices = await self._api.get_devices()

    async def _async_update_data(self) -> dict[str, LastData]:
        if not self._logged_in:
            await self._login_and_list_devices()
        try:
            return {
                device.serial_number: await self._api.get_last_data(device)
                for device in self.devices
            }
        except ShineMonitorAuthError as err:
            self._logged_in = False
            raise ConfigEntryAuthFailed(str(err)) from err
        except Exception as err:
            self._logged_in = False
            raise UpdateFailed(str(err)) from err
