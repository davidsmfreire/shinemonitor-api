"""Synchronous client over httpx.Client."""

from __future__ import annotations

import logging
from datetime import date
from types import TracebackType
from typing import Any

import httpx

from . import _protocol as _p
from ._methods import SyncActionsMixin
from .models import DeviceIdentifier, LastData

_LOGGER = logging.getLogger(__name__)
_DEFAULT_TIMEOUT = 10.0


class ShineMonitorAPI(SyncActionsMixin):
    """Synchronous client for the ShineMonitor REST API.

    Inherits 30+ generated `query_*` / `ctrl_*` action methods from
    `SyncActionsMixin`; overrides the few that need bespoke parsing
    (login, get_devices, get_last_data, get_daily_data).
    """

    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        timeout: float = _DEFAULT_TIMEOUT,
        base_url: str | None = None,
        suffix_context: str | None = None,
        company_key: str | None = None,
    ) -> None:
        self._http = client or httpx.Client(timeout=timeout)
        self._owns_http = client is None
        self._auth: _p.AuthState | None = None
        self._config = _p.ProtocolConfig(
            base_url=base_url or _p.DEFAULT_BASE_URL,
            suffix_context=suffix_context or _p.WATCHPOWER_SUFFIX_CONTEXT,
            company_key=company_key or _p.WATCHPOWER_COMPANY_KEY,
        )

    def __enter__(self) -> ShineMonitorAPI:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_http:
            self._http.close()

    @property
    def auth(self) -> _p.AuthState | None:
        return self._auth

    def login(self, username: str, password: str) -> ShineMonitorAPI:
        payload = self._get_json(_p.login_url(self._config, username, password))
        self._auth = _p.parse_login(payload)
        _LOGGER.debug("ShineMonitor login successful")
        return self

    def get_devices(self) -> list[DeviceIdentifier]:
        return _p.parse_devices(
            self._get_json(_p.devices_url(self._config, self._require_auth()))
        )

    def get_last_data(self, device: DeviceIdentifier) -> LastData:
        return _p.parse_last(
            self._get_json(_p.last_data_url(self._config, self._require_auth(), device))
        )

    def get_daily_data(
        self,
        day: date,
        serial_number: str,
        wifi_pn: str,
        dev_code: int,
        dev_addr: int,
    ) -> dict[str, Any]:
        return _p.parse_daily_data(
            self._get_json(
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
        )

    def get_device_daily_data(
        self, device: DeviceIdentifier, day: date
    ) -> dict[str, Any]:
        return self.get_daily_data(
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

    def _get_json(self, url: str) -> dict[str, Any]:
        response = self._http.get(url)
        response.raise_for_status()
        return response.json()
