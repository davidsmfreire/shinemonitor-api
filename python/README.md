# ShineMonitor API in Python

ShineMonitor is the cloud backend (`api.shinemonitor.com`) used by several
inverter vendor apps — WatchPower, SolarPower, etc. By decompiling the
WatchPower Android APK with Jadx, the authentication flow was
reverse-engineered, giving direct access to the backend REST API for
programmatic inverter queries.

```shell
pip install shinemonitor-api
```

Check the `examples/` folder for usage. To run the examples or develop
the library, use [uv](https://docs.astral.sh/uv/):

```shell
uv sync --all-groups
```

That installs all dependencies, including the optional `examples` group.

## Sync and async

Two thin I/O shells over a shared sansio core (URL building, signing,
parsing). Pick whichever fits the calling code — both expose the same
methods.

```python
# sync
from shinemonitor_api import ShineMonitorAPI

with ShineMonitorAPI() as api:
    api.login(username, password)
    devices = api.get_devices()
    for device in devices:
        print(api.get_last_data(device).main)
```

```python
# async
import asyncio
from shinemonitor_api.aio import AsyncShineMonitorAPI

async def main():
    async with AsyncShineMonitorAPI() as api:
        await api.login(username, password)
        devices = await api.get_devices()
        snapshots = await asyncio.gather(
            *(api.get_last_data(d) for d in devices)
        )
        for snapshot in snapshots:
            print(snapshot.main)

asyncio.run(main())
```

Both clients accept an `httpx.Client` / `httpx.AsyncClient` for reuse
in apps that already manage one (e.g. Home Assistant).

## Targeting a different vendor app

The ShineMonitor backend is shared by many white-label apps (WatchPower,
RenoClient / Renovigi, ...). Devices are scoped to the app that registered
them, so pass the matching profile — WatchPower is the default.

```python
from shinemonitor_api import ShineMonitorAPI, AppProfile

# a shipped preset
with ShineMonitorAPI(app=AppProfile.RENOCLIENT) as api:
    api.login(username, password)
    devices = api.get_devices()

# an app without a preset — supply its identifiers
custom = AppProfile(app_id="com.example.app", app_version="1.0.0")
api = ShineMonitorAPI(app=custom)
```

`AppProfile.from_name("renoclient")` resolves a shipped preset by name
(handy when the app is chosen from config). `get_devices()` automatically
falls back from the undocumented `webQueryDeviceEs` action to the
documented `queryDevices` when the former reports no devices.

## Migrating from `watchpower-api`

`watchpower-api` is the previous PyPI name. The package was renamed to
`shinemonitor-api` because the upstream API serves more than just the
WatchPower app. The `WatchPowerAPI` class is now `ShineMonitorAPI`.

```python
# before
from watchpower_api import WatchPowerAPI

# after
from shinemonitor_api import ShineMonitorAPI
```
