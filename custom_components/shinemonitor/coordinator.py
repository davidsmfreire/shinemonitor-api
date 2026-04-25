"""DataUpdateCoordinator for ShineMonitor."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from shinemonitor_api import ShineMonitorAPI
from shinemonitor_api.models import DeviceIdentifier, LastData

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
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
        self._api: ShineMonitorAPI | None = None
        self.devices: list[DeviceIdentifier] = []

    async def _async_setup(self) -> None:
        """One-time login and device enumeration."""
        await self.hass.async_add_executor_job(self._login_and_list_devices)

    def _login_and_list_devices(self) -> None:
        api = ShineMonitorAPI()
        try:
            api.login(self._username, self._password)
        except RuntimeError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        self._api = api
        self.devices = api.get_devices()

    async def _async_update_data(self) -> dict[str, LastData]:
        if self._api is None:
            await self._async_setup()
        try:
            return await self.hass.async_add_executor_job(self._fetch_all)
        except RuntimeError as err:
            # Token may have expired — clear so next tick re-logs in.
            self._api = None
            raise UpdateFailed(str(err)) from err

    def _fetch_all(self) -> dict[str, LastData]:
        assert self._api is not None
        return {
            device.serial_number: self._api.get_last_data(device)
            for device in self.devices
        }
