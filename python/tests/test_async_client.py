"""End-to-end tests of the async client against the FastAPI mock."""

from __future__ import annotations

import asyncio
from datetime import date

import pytest

from shinemonitor_api import AppProfile, ShineMonitorAuthError
from shinemonitor_api.aio import AsyncShineMonitorAPI

from shinemonitor_mock import VALID_PASSWORD, VALID_USERNAME


async def test_login_success(async_http, client_kwargs) -> None:
    api = AsyncShineMonitorAPI(client=async_http, **client_kwargs)
    await api.login(VALID_USERNAME, VALID_PASSWORD)
    assert api.auth is not None
    assert api.auth.token == "tok-12345"


async def test_login_bad_password(async_http, client_kwargs) -> None:
    api = AsyncShineMonitorAPI(client=async_http, **client_kwargs)
    with pytest.raises(ShineMonitorAuthError) as excinfo:
        await api.login(VALID_USERNAME, "wrong")
    assert excinfo.value.err == 0x0010


async def test_get_devices_then_last_data(async_http, client_kwargs) -> None:
    api = AsyncShineMonitorAPI(client=async_http, **client_kwargs)
    await api.login(VALID_USERNAME, VALID_PASSWORD)
    devices = await api.get_devices()
    snapshots = await asyncio.gather(*(api.get_last_data(d) for d in devices))
    assert {s.main.battery_capacity for s in snapshots} == {85, 65}


async def test_get_devices_falls_back_to_query_devices_on_258(
    async_http, base_url
) -> None:
    # RenoClient-scoped device: webQueryDeviceEs → 258, queryDevices serves it.
    api = AsyncShineMonitorAPI(
        client=async_http,
        app=AppProfile(
            app_id="com.eybond.renoclient",
            app_version="1.3.2.0",
            company_key="test-company",
            base_url=base_url,
        ),
    )
    await api.login(VALID_USERNAME, VALID_PASSWORD)
    devices = await api.get_devices()
    assert len(devices) == 2
    assert devices[0].serial_number == "9620230101001"


async def test_get_daily_data(async_http, client_kwargs) -> None:
    api = AsyncShineMonitorAPI(client=async_http, **client_kwargs)
    await api.login(VALID_USERNAME, VALID_PASSWORD)
    devices = await api.get_devices()
    raw = await api.get_device_daily_data(devices[0], date(2026, 4, 25))
    assert raw["err"] == 0
    assert len(raw["dat"]["row"]) == 2


async def test_unauthed_call_raises(async_http, client_kwargs) -> None:
    api = AsyncShineMonitorAPI(client=async_http, **client_kwargs)
    with pytest.raises(ShineMonitorAuthError):
        await api.get_devices()
