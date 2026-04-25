"""Language-agnostic mock of the ShineMonitor REST API.

Mirrors the documented contract at https://api.shinemonitor.com/:

* Single endpoint at `/public/` accepting GET with a query string.
* `action` selects the operation; `salt` + `sign` verify the request.
* Authed actions additionally require `token`; signature is then
  `SHA-1(salt + secret + token + base_action)`.
* Auth signature is `SHA-1(salt + SHA-1(pwd) + base_action)` for the
  documented `auth` action and the variant `authSource` used by the
  WatchPower app.

Usable two ways:

1. **In-process** (Python tests): `from shinemonitor_mock import create_app`
   and pass to httpx's ASGI transport.
2. **Subprocess** (any language): `python -m shinemonitor_mock --port 0`
   prints `LISTENING http://127.0.0.1:<port>/` to stdout, then serves
   until killed.

Fixture credentials and fixture data are exposed as module constants so
test code can import them without restating magic strings.
"""

from __future__ import annotations

import hashlib
from typing import Any

from fastapi import FastAPI, Request

# --- Canonical fixture data ------------------------------------------------

VALID_USERNAME = "demo-user"
VALID_PASSWORD = "demo-pass"
VALID_COMPANY_KEY = "test-company"
ISSUED_TOKEN = "tok-12345"
ISSUED_SECRET = "sec-67890"
TOKEN_EXPIRES = 604800

DEVICES: list[dict[str, Any]] = [
    {
        "devalias": "Inverter Garage",
        "sn": "9620230101001",
        "pn": "W0001234",
        "devaddr": 1,
        "devcode": 2451,
    },
    {
        "devalias": None,
        "sn": "9620230101002",
        "pn": "W0001235",
        "devaddr": 1,
        "devcode": 2451,
    },
]

LAST_DATA_BY_SN: dict[str, dict[str, Any]] = {
    "9620230101001": {
        "dat": {
            "gts": "2026-04-25 09:00:00",
            "pars": {
                "gd_": [
                    {"id": "gd_grid_rating_voltage", "val": "230.0"},
                    {"id": "gd_grid_rating_current", "val": "30.0"},
                    {"id": "gd_battery_rating_voltage", "val": "48.0"},
                    {"id": "gd_bse_input_voltage_read", "val": "230.0"},
                    {"id": "gd_ac_output_rating_current", "val": "30.0"},
                    {"id": "gd_bse_output_frequency_read", "val": "50.0"},
                    {"id": "gd_ac_output_rating_apparent_power", "val": "5000"},
                    {"id": "gd_ac_output_rating_active_power", "val": "5000"},
                ],
                "sy_": [
                    {"id": "sy_model", "val": "5KW Inverter"},
                    {"id": "sy_main_cpu1_firmware_version", "val": "01.23"},
                    {"id": "sy_main_cpu2_firmware_version", "val": "04.56"},
                ],
                "pv_": [
                    {"id": "pv_input_current", "val": "12.5"},
                ],
                "bt_": [
                    {"id": "bt_grid_voltage", "val": "229.5"},
                    {"id": "bt_grid_frequency", "val": "50.0"},
                    {"id": "bt_voltage_1", "val": "180.2"},
                    {"id": "bt_input_power", "val": "1500"},
                    {"id": "bt_battery_voltage", "val": "52.4"},
                    {"id": "bt_battery_capacity", "val": "85"},
                    {"id": "bt_battery_charging_current", "val": "10.5"},
                    {"id": "bt_battery_discharge_current", "val": "0.0"},
                    {"id": "bt_ac_output_voltage", "val": "230.1"},
                    {"id": "bt_grid_AC_frequency", "val": "50.0"},
                    {"id": "bt_ac_output_apparent_power", "val": "1200"},
                    {"id": "bt_load_active_power_sole", "val": "1100"},
                    {"id": "bt_output_load_percent", "val": "22"},
                ],
            },
        }
    },
    "9620230101002": {
        "dat": {
            "gts": "2026-04-25 09:00:05",
            "pars": {
                "gd_": [
                    {"id": "gd_grid_rating_voltage", "val": "230.0"},
                    {"id": "gd_grid_rating_current", "val": "30.0"},
                    {"id": "gd_battery_rating_voltage", "val": "48.0"},
                    {"id": "gd_bse_input_voltage_read", "val": "230.0"},
                    {"id": "gd_ac_output_rating_current", "val": "30.0"},
                    {"id": "gd_bse_output_frequency_read", "val": "50.0"},
                    {"id": "gd_ac_output_rating_apparent_power", "val": "5000"},
                    {"id": "gd_ac_output_rating_active_power", "val": "5000"},
                ],
                "sy_": [
                    {"id": "sy_model", "val": "5KW Inverter"},
                    {"id": "sy_main_cpu1_firmware_version", "val": "01.23"},
                    {"id": "sy_main_cpu2_firmware_version", "val": "04.56"},
                ],
                "pv_": [
                    {"id": "pv_input_current", "val": "8.0"},
                ],
                "bt_": [
                    {"id": "bt_grid_voltage", "val": "230.0"},
                    {"id": "bt_grid_frequency", "val": "50.0"},
                    {"id": "bt_voltage_1", "val": "0.0"},
                    {"id": "bt_input_power", "val": "0"},
                    {"id": "bt_battery_voltage", "val": "49.8"},
                    {"id": "bt_battery_capacity", "val": "65"},
                    {"id": "bt_battery_charging_current", "val": "0.0"},
                    {"id": "bt_battery_discharge_current", "val": "5.5"},
                    {"id": "bt_ac_output_voltage", "val": "230.0"},
                    {"id": "bt_grid_AC_frequency", "val": "50.0"},
                    {"id": "bt_ac_output_apparent_power", "val": "800"},
                    {"id": "bt_load_active_power_sole", "val": "780"},
                    {"id": "bt_output_load_percent", "val": "16"},
                ],
            },
        }
    },
}

DAILY_DATA_TITLES: list[dict[str, Any]] = [
    {"title": "time", "unit": ""},
    {"title": "battery_voltage", "unit": "V"},
    {"title": "ac_output_active_power", "unit": "W"},
]
DAILY_DATA_ROWS: list[dict[str, Any]] = [
    {"realtime": True, "field": ["09:00:00", "52.4", "1100"]},
    {"realtime": True, "field": ["09:05:00", "52.5", "1150"]},
]

# --- Server ----------------------------------------------------------------


def _sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest().lower()  # nosec - vendor-mandated


def _hash(*parts: str) -> str:
    return _sha1("".join(parts).encode("utf-8"))


def _err(code: int, desc: str) -> dict[str, Any]:
    return {"err": code, "desc": desc}


def _ok(data: Any) -> dict[str, Any]:
    return {"err": 0, "desc": "ERR_NONE", "dat": data}


def _base_action(request: Request, exclude: set[str]) -> str:
    raw = request.scope["query_string"].decode("ascii")
    pairs = [pair for pair in raw.split("&") if pair]
    kept = [pair for pair in pairs if pair.split("=", 1)[0] not in exclude]
    return "&" + "&".join(kept) if kept else ""


def create_app() -> FastAPI:
    """Build the FastAPI app. Each call returns a fresh instance."""
    app = FastAPI(title="ShineMonitor mock")

    @app.get("/public/")
    async def public(request: Request) -> dict[str, Any]:
        params = dict(request.query_params)
        salt = params.get("salt")
        sign = params.get("sign")
        action = params.get("action")
        if not salt or not sign or not action:
            return _err(0x0007, "ERR_PARAMETER_VALUE_BAD")

        if action in ("auth", "authSource"):
            return _handle_auth(request, params, salt, sign)

        token = params.get("token")
        if not token:
            return _err(0x0007, "ERR_PARAMETER_VALUE_BAD")
        if token != ISSUED_TOKEN:
            return _err(0x010E, "ERR_TOKEN_INVALID")

        base_action = _base_action(request, {"sign", "salt", "token"})
        if sign != _hash(salt, ISSUED_SECRET, token, base_action):
            return _err(0x0007, "ERR_PARAMETER_VALUE_BAD")

        if action == "webQueryDeviceEs":
            return _ok({"device": DEVICES})
        if action == "querySPDeviceLastData":
            sn = params.get("sn", "")
            snapshot = LAST_DATA_BY_SN.get(sn)
            if snapshot is None:
                return _err(0x0102, "ERR_DEVICE_NOT_FOUND")
            return {"err": 0, "desc": "ERR_NONE", **snapshot}
        if action == "queryDeviceDataOneDay":
            return _ok({"title": DAILY_DATA_TITLES, "row": DAILY_DATA_ROWS})

        return _err(0x0001, "ERR_UNKNOWN_ACTION")

    return app


def _handle_auth(
    request: Request, params: dict[str, str], salt: str, sign: str
) -> dict[str, Any]:
    usr = params.get("usr")
    company_key = params.get("company-key")
    if not usr or not company_key:
        return _err(0x0007, "ERR_PARAMETER_VALUE_BAD")
    if company_key != VALID_COMPANY_KEY:
        return _err(0x000F, "ERR_NO_MANUFACTURER")

    base_action = _base_action(request, {"sign", "salt"})
    expected = _hash(salt, _hash(VALID_PASSWORD), base_action)
    if sign != expected:
        if usr != VALID_USERNAME:
            return _err(0x0105, "ERR_USER_NOT_EXIST")
        return _err(0x0010, "ERR_PASSWORD_ERROR")

    if usr != VALID_USERNAME:
        return _err(0x0105, "ERR_USER_NOT_EXIST")

    return _ok(
        {
            "secret": ISSUED_SECRET,
            "expire": TOKEN_EXPIRES,
            "token": ISSUED_TOKEN,
            "role": 0,
        }
    )
