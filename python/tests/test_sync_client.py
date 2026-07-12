"""End-to-end tests of the sync client against the FastAPI mock."""

from __future__ import annotations

from datetime import date

import pytest

from shinemonitor_api import AppProfile, ShineMonitorAPI, ShineMonitorAuthError

from shinemonitor_mock import VALID_PASSWORD, VALID_USERNAME


def test_login_success(sync_http, client_kwargs) -> None:
    api = ShineMonitorAPI(client=sync_http, **client_kwargs)
    api.login(VALID_USERNAME, VALID_PASSWORD)
    assert api.auth is not None
    assert api.auth.token == "tok-12345"
    assert api.auth.secret == "sec-67890"
    assert api.auth.expire == 604800


def test_login_bad_password(sync_http, client_kwargs) -> None:
    api = ShineMonitorAPI(client=sync_http, **client_kwargs)
    with pytest.raises(ShineMonitorAuthError) as excinfo:
        api.login(VALID_USERNAME, "wrong")
    assert excinfo.value.err == 0x0010


def test_login_unknown_user(sync_http, client_kwargs) -> None:
    api = ShineMonitorAPI(client=sync_http, **client_kwargs)
    with pytest.raises(ShineMonitorAuthError) as excinfo:
        api.login("nobody", VALID_PASSWORD)
    assert excinfo.value.err == 0x0105


def test_login_bad_company_key(sync_http, base_url) -> None:
    api = ShineMonitorAPI(
        client=sync_http,
        app=AppProfile(
            app_id="test.app",
            app_version="0.0.1",
            company_key="not-the-right-key",
            base_url=base_url,
        ),
    )
    with pytest.raises(ShineMonitorAuthError) as excinfo:
        api.login(VALID_USERNAME, VALID_PASSWORD)
    assert excinfo.value.err == 0x000F


def test_get_devices(sync_http, client_kwargs) -> None:
    api = ShineMonitorAPI(client=sync_http, **client_kwargs)
    api.login(VALID_USERNAME, VALID_PASSWORD)
    devices = api.get_devices()
    assert len(devices) == 2
    assert devices[0].serial_number == "9620230101001"
    assert devices[0].device_alias == "Inverter Garage"
    assert devices[1].device_alias is None


def test_get_devices_falls_back_to_query_devices_on_258(sync_http, base_url) -> None:
    # RenoClient-scoped device: webQueryDeviceEs → 258, queryDevices serves it.
    api = ShineMonitorAPI(
        client=sync_http,
        app=AppProfile(
            app_id="com.eybond.renoclient",
            app_version="1.3.2.0",
            company_key="test-company",
            base_url=base_url,
        ),
    )
    api.login(VALID_USERNAME, VALID_PASSWORD)
    devices = api.get_devices()
    assert len(devices) == 2
    assert devices[0].serial_number == "9620230101001"


def test_get_last_data(sync_http, client_kwargs) -> None:
    api = ShineMonitorAPI(client=sync_http, **client_kwargs)
    api.login(VALID_USERNAME, VALID_PASSWORD)
    devices = api.get_devices()
    snapshot = api.get_last_data(devices[0])
    assert snapshot.main.battery_capacity == 85
    assert snapshot.main.ac_output_active_power == 1100
    assert snapshot.system.model == "5KW Inverter"


def test_get_daily_data(sync_http, client_kwargs) -> None:
    api = ShineMonitorAPI(client=sync_http, **client_kwargs)
    api.login(VALID_USERNAME, VALID_PASSWORD)
    devices = api.get_devices()
    raw = api.get_device_daily_data(devices[0], date(2026, 4, 25))
    assert raw["err"] == 0
    assert len(raw["dat"]["row"]) == 2


def test_unauthed_call_raises(sync_http, client_kwargs) -> None:
    api = ShineMonitorAPI(client=sync_http, **client_kwargs)
    with pytest.raises(ShineMonitorAuthError):
        api.get_devices()
