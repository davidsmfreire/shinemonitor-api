"""Sansio (no I/O) layer: URL builders and response parsers.

Both the sync and async clients call into this module for everything
that does not touch the network. Keeps a single source of truth for
auth, signing, and decoding.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from datetime import date
from typing import Any

from .models import DeviceIdentifier, LastData, parse_last_data

DEFAULT_BASE_URL: str = "http://android.shinemonitor.com/public/"
DEFAULT_SUFFIX_CONTEXT: str = (
    "&i18n=pt_BR&lang=pt_BR&source=1"
    "&_app_client_=android&_app_id_=wifiapp.volfw.watchpower"
    "&_app_version_=1.0.6.3"
)
DEFAULT_COMPANY_KEY: str = "bnrl_frRFjEz8Mkn"


@dataclass(frozen=True)
class AuthState:
    """Result of a successful login — what subsequent requests sign with."""

    token: str
    secret: str
    expire: int


@dataclass(frozen=True)
class ProtocolConfig:
    """Per-client configuration for URL building.

    Defaults match the WatchPower Android app context. Tests and
    alternate-app callers can override.
    """

    base_url: str = DEFAULT_BASE_URL
    suffix_context: str = DEFAULT_SUFFIX_CONTEXT
    company_key: str = DEFAULT_COMPANY_KEY


def _salt() -> str:
    return str(round(time.time() * 1000))


def _sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest().lower()  # nosec - vendor-mandated


def _hash(*parts: str) -> str:
    return _sha1("".join(parts).encode("utf-8"))


def login_url(config: ProtocolConfig, username: str, password: str) -> str:
    base_action = (
        f"&action=authSource&usr={username}"
        f"&company-key={config.company_key}{config.suffix_context}"
    )
    salt = _salt()
    sign = _hash(salt, _hash(password), base_action)
    return f"{config.base_url}?sign={sign}&salt={salt}{base_action}"


def authed_url(config: ProtocolConfig, auth: AuthState, base_action: str) -> str:
    """Sign and assemble an authed request URL.

    Public so that the generated `_actions.py` can call it without
    reaching past a leading underscore.
    """
    salt = _salt()
    sign = _hash(salt, auth.secret, auth.token, base_action)
    return f"{config.base_url}?sign={sign}&salt={salt}&token={auth.token}{base_action}"


# Back-compat alias for handwritten callers in this module.
_authed_url = authed_url


def devices_url(config: ProtocolConfig, auth: AuthState) -> str:
    return _authed_url(config, auth, f"&action=webQueryDeviceEs{config.suffix_context}")


def last_data_url(
    config: ProtocolConfig, auth: AuthState, device: DeviceIdentifier
) -> str:
    base_action = (
        f"&action=querySPDeviceLastData"
        f"&pn={device.wifi_pin}&devcode={device.device_code}"
        f"&sn={device.serial_number}&devaddr={device.device_address}"
        f"{config.suffix_context}"
    )
    return _authed_url(config, auth, base_action)


def daily_data_url(
    config: ProtocolConfig,
    auth: AuthState,
    day: date,
    serial_number: str,
    wifi_pn: str,
    dev_code: int,
    dev_addr: int,
) -> str:
    base_action = (
        f"&action=queryDeviceDataOneDay"
        f"&pn={wifi_pn}&devcode={dev_code}&sn={serial_number}&devaddr={dev_addr}"
        f"&date={day.isoformat()}{config.suffix_context}"
    )
    return _authed_url(config, auth, base_action)


class ShineMonitorError(RuntimeError):
    """API returned a non-zero `err` code."""

    def __init__(self, payload: dict[str, Any]) -> None:
        super().__init__(payload)
        self.err: int = int(payload.get("err", -1))
        self.desc: str = str(payload.get("desc", ""))
        self.payload: dict[str, Any] = payload


class ShineMonitorAuthError(ShineMonitorError):
    """Login or signing failed — credentials likely invalid or expired."""


# Documented auth-band error codes from chapter 2 (auth.html). Hex in docs,
# integers on the wire.
_AUTH_ERR_CODES: frozenset[int] = frozenset(
    {
        0x0007,  # missing required parameters (often signals signature error)
        0x000F,  # manufacturer key not found
        0x0010,  # password verification failure
        0x0019,  # account frozen
        0x0105,  # user account not found
        0x010E,  # token expired (commonly observed; treat as auth so callers re-login)
    }
)


def check_response(payload: dict[str, Any]) -> dict[str, Any]:
    """Raise if the vendor `err` is non-zero, else return the payload.

    Public so the generated `_actions.py` parsers can reuse the same
    error-band logic the handwritten parsers use.
    """
    err = payload.get("err")
    if err == 0:
        return payload
    if isinstance(err, int) and err in _AUTH_ERR_CODES:
        raise ShineMonitorAuthError(payload)
    raise ShineMonitorError(payload)


# Back-compat alias for handwritten callers in this module.
_check = check_response


def parse_login(payload: dict[str, Any]) -> AuthState:
    data = _check(payload)["dat"]
    return AuthState(
        token=data["token"],
        secret=data["secret"],
        expire=int(data["expire"]),
    )


def parse_devices(payload: dict[str, Any]) -> list[DeviceIdentifier]:
    data = _check(payload)["dat"]
    return [DeviceIdentifier(**raw) for raw in data["device"]]


def parse_daily_data(payload: dict[str, Any]) -> dict[str, Any]:
    return _check(payload)


def parse_last(payload: dict[str, Any]) -> LastData:
    return parse_last_data(_check(payload))
