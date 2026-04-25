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
