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
