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

BASE_URL: str = "http://android.shinemonitor.com/public/"
SUFFIX_CONTEXT: str = (
    "&i18n=pt_BR&lang=pt_BR&source=1"
    "&_app_client_=android&_app_id_=wifiapp.volfw.watchpower"
    "&_app_version_=1.0.6.3"
)
COMPANY_KEY: str = "bnrl_frRFjEz8Mkn"


@dataclass(frozen=True)
class AuthState:
    """Result of a successful login — what subsequent requests sign with."""

    token: str
    secret: str
    expire: int


def _salt() -> str:
    return str(round(time.time() * 1000))


def _sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest().lower()  # nosec - vendor-mandated


def _hash(*parts: str) -> str:
    return _sha1("".join(parts).encode("utf-8"))


def login_url(username: str, password: str) -> str:
    base_action = (
        f"&action=authSource&usr={username}&company-key={COMPANY_KEY}{SUFFIX_CONTEXT}"
    )
    salt = _salt()
    sign = _hash(salt, _hash(password), base_action)
    return f"{BASE_URL}?sign={sign}&salt={salt}{base_action}"


def _authed_url(auth: AuthState, base_action: str) -> str:
    salt = _salt()
    sign = _hash(salt, auth.secret, auth.token, base_action)
    return f"{BASE_URL}?sign={sign}&salt={salt}&token={auth.token}{base_action}"


def devices_url(auth: AuthState) -> str:
    return _authed_url(auth, f"&action=webQueryDeviceEs{SUFFIX_CONTEXT}")


def last_data_url(auth: AuthState, device: DeviceIdentifier) -> str:
    base_action = (
        f"&action=querySPDeviceLastData"
        f"&pn={device.wifi_pin}&devcode={device.device_code}"
        f"&sn={device.serial_number}&devaddr={device.device_address}"
        f"{SUFFIX_CONTEXT}"
    )
    return _authed_url(auth, base_action)


def daily_data_url(
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
        f"&date={day.isoformat()}{SUFFIX_CONTEXT}"
    )
    return _authed_url(auth, base_action)


class ShineMonitorError(RuntimeError):
    """API returned a non-zero `err` code."""


class ShineMonitorAuthError(ShineMonitorError):
    """Login or signing failed — credentials likely invalid or expired."""


def _check(payload: dict[str, Any]) -> dict[str, Any]:
    err = payload.get("err")
    if err == 0:
        return payload
    # The vendor uses small integers; treat anything in the auth band as auth failure.
    if err in (1, 2, 10004, 10005, 10008):
        raise ShineMonitorAuthError(payload)
    raise ShineMonitorError(payload)


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
