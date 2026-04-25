"""Round-trip every generated action through the mock.

Confirms that for each entry in `spec/endpoints.yaml`:
- the generated `url_*` builder produces a signed URL the mock accepts,
- the generated mock handler returns `err == 0`,
- the generated `parse_*` function consumes that response without
  raising.

Args for required parameters are synthesized — the mock ignores them
because canned responses don't depend on inputs. For real payload
shapes, add explicit assertions in `test_sync_client.py` instead.
"""

from __future__ import annotations

import inspect
from collections.abc import Iterable
from typing import Any

import pytest

from shinemonitor_api import ShineMonitorAPI
from shinemonitor_api._methods import SyncActionsMixin

from shinemonitor_mock import VALID_PASSWORD, VALID_USERNAME

_SYNTH: dict[str, Any] = {
    "status": 1,
    "orderBy": "ascPlantName",
    "plantName": "demo",
    "page": 0,
    "pagesize": 1,
    "plantid": 1,
    "pn": "W0001234",
    "devcode": 2451,
    "devaddr": 1,
    "sn": "9620230101001",
    "date": "2026-04-25",
    "id": "field_id",
    "val": "1",
    "oldPwd": "x",
    "newPwd": "y",
    "fmt": "jpg",
    "cameraid": 1,
}


def _generated_methods() -> Iterable[tuple[str, inspect.Signature]]:
    for name in dir(SyncActionsMixin):
        if name.startswith("_"):
            continue
        attr = getattr(SyncActionsMixin, name)
        if not callable(attr):
            continue
        sig = inspect.signature(attr)
        yield name, sig


def _kwargs_for(sig: inspect.Signature) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for pname, param in sig.parameters.items():
        if pname == "self":
            continue
        if param.default is not inspect.Parameter.empty:
            continue  # skip optional — exercises the "no extras" path
        out[pname] = _SYNTH[pname]
    return out


@pytest.mark.parametrize("method_name", [name for name, _ in _generated_methods()])
def test_generated_action_round_trip(
    sync_http, client_kwargs, method_name: str
) -> None:
    api = ShineMonitorAPI(client=sync_http, **client_kwargs)
    api.login(VALID_USERNAME, VALID_PASSWORD)

    method = getattr(api, method_name)
    sig = inspect.signature(method)
    payload = method(**_kwargs_for(sig))

    assert isinstance(payload, dict)
    assert payload.get("err") == 0
