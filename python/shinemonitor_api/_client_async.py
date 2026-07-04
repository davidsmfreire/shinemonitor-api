"""Asynchronous client over httpx.AsyncClient."""

from __future__ import annotations

import json
import logging
from datetime import date
from types import TracebackType
from typing import Any

import httpx

from . import _protocol as _p
from ._methods import AsyncActionsMixin
from .models import DeviceIdentifier, LastData

_LOGGER = logging.getLogger(__name__)
_DEFAULT_TIMEOUT = 10.0


class AsyncShineMonitorAPI(AsyncActionsMixin):
    """Asynchronous client for the ShineMonitor REST API.

    Inherits 30+ generated `query_*` / `ctrl_*` action methods from
    `AsyncActionsMixin`; overrides the few that need bespoke parsing.
    """

    def __init__(
        self,
        *,
        app: _p.AppProfile = _p.AppProfile.WATCHPOWER,
        client: httpx.AsyncClient | None = None,
        timeout: float = _DEFAULT_TIMEOUT,
    ) -> None:
        self._http = client or httpx.AsyncClient(timeout=timeout)
        self._owns_http = client is None
        self._auth: _p.AuthState | None = None
        self._app = app
        self._config = app._to_config()

    async def __aenter__(self) -> AsyncShineMonitorAPI:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_http:
            await self._http.aclose()

    @property
    def auth(self) -> _p.AuthState | None:
        return self._auth

    async def login(self, username: str, password: str) -> AsyncShineMonitorAPI:
        payload = await self._get_json(_p.login_url(self._config, username, password))
        self._auth = _p.parse_login(payload)
        _LOGGER.debug("ShineMonitor login successful")
        return self

    async def get_devices(self) -> list[DeviceIdentifier]:
        auth = self._require_auth()
        last_exc: _p.ShineMonitorError | None = None

        apps_to_try: list[_p.AppProfile] = [self._app]
        for known_app in _p.KNOWN_APPS.values():
            if known_app.app_id != self._app.app_id:
                apps_to_try.append(
                    _p.AppProfile(
                        app_id=known_app.app_id,
                        app_version=known_app.app_version,
                        company_key=self._app.company_key,
                        base_url=self._app.base_url,
                        locale=self._app.locale,
                        source=self._app.source,
                        app_client=self._app.app_client,
                    )
                )

        for app in apps_to_try:
            config = app._to_config()
            try:
                payload = await self._get_json(_p.devices_url(config, auth))
                return _p.parse_devices(payload)
            except _p.ShineMonitorError as exc:
                if exc.err != 0x0102:
                    raise
                last_exc = exc
                _LOGGER.debug(
                    "webQueryDeviceEs returned ERR_NOT_FOUND_DEVICE "
                    "for app %s; trying next profile",
                    app.app_id,
                )

        raise last_exc  # type: ignore[misc]

    async def get_last_data(self, device: DeviceIdentifier) -> LastData:
        payload = await self._get_json(
            _p.last_data_url(self._config, self._require_auth(), device)
        )
        return _p.parse_last(payload)

    async def get_daily_data(
        self,
        day: date,
        serial_number: str,
        wifi_pn: str,
        dev_code: int,
        dev_addr: int,
    ) -> dict[str, Any]:
        payload = await self._get_json(
            _p.daily_data_url(
                self._config,
                self._require_auth(),
                day,
                serial_number,
                wifi_pn,
                dev_code,
                dev_addr,
            )
        )
        return _p.parse_daily_data(payload)

    async def get_device_daily_data(
        self, device: DeviceIdentifier, day: date
    ) -> dict[str, Any]:
        return await self.get_daily_data(
            day=day,
            serial_number=device.serial_number,
            wifi_pn=device.wifi_pin,
            dev_code=device.device_code,
            dev_addr=device.device_address,
        )

    def _require_auth(self) -> _p.AuthState:
        if self._auth is None:
            raise _p.ShineMonitorAuthError(
                {"err": -1, "desc": "Not logged in — call .login() first"}
            )
        return self._auth

    async def _get_json(self, url: str) -> Any:
        response = await self._http.get(url)
        response.raise_for_status()
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text
