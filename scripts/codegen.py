#!/usr/bin/env python3
"""Drive sansio URL builders + parsers and mock handlers from spec/endpoints.yaml.

Outputs:
  python/shinemonitor_api/_actions.py       — typed URL builders + parsers
  mock-server/shinemonitor_mock/_actions.py — canned-response handlers

Auth flows (`auth`, `authSource`) stay handwritten in `_protocol.py`
and `server.py` because their signing scheme is different. Codegen
covers everything that uses the standard `authed_url` shape.

Re-run from repo root after spec edits:
    python scripts/codegen.py
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC_FILE = ROOT / "spec" / "endpoints.yaml"
PY_OUT = ROOT / "python" / "shinemonitor_api" / "_actions.py"
PY_METHODS_OUT = ROOT / "python" / "shinemonitor_api" / "_methods.py"
MOCK_OUT = ROOT / "mock-server" / "shinemonitor_mock" / "_actions.py"

PY_TYPE_MAP = {
    "string": "str",
    "int": "int",
    "float": "float",
    "bool": "bool",
}

AUTH_ACTIONS = {"auth", "authSource"}


def _snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _py_param(p: dict[str, Any]) -> str:
    name = p["name"].replace("-", "_")
    py_type = PY_TYPE_MAP.get(p["type"], "str")
    if p.get("required", True):
        return f"{name}: {py_type}"
    return f"{name}: {py_type} | None = None"


def render_python(spec: dict[str, Any]) -> str:
    lines = [
        '"""GENERATED — do not edit. Run `python scripts/codegen.py`."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "from . import _protocol as _p",
        "",
    ]

    for ep in spec["endpoints"]:
        action = ep["action"]
        if action in AUTH_ACTIONS:
            continue
        snake = _snake(action)
        params = ep.get("params", [])

        sig_params = ["config: _p.ProtocolConfig", "auth: _p.AuthState"]
        sig_params.extend(_py_param(p) for p in params)

        # Required params build the static portion of base_action; optional
        # params append themselves at runtime if non-None.
        static_parts = [f"&action={action}"]
        for p in params:
            if not p.get("required", True):
                continue
            vendor = p["name"]
            py_name = vendor.replace("-", "_")
            static_parts.append(f"&{vendor}={{{py_name}}}")
        static_parts.append("{config.suffix_context}")
        static_template = "".join(static_parts)

        body: list[str] = [
            f'    base_action = f"{static_template}"',
        ]
        for p in params:
            if p.get("required", True):
                continue
            vendor = p["name"]
            py_name = vendor.replace("-", "_")
            body.append(f"    if {py_name} is not None:")
            body.append(f'        base_action += f"&{vendor}={{{py_name}}}"')
        body.append("    return _p.authed_url(config, auth, base_action)")

        lines.append("")
        lines.append(f"def url_{snake}({', '.join(sig_params)}) -> str:")
        lines.append(f'    """Action `{action}` — chapter {ep.get("chapter", "?")}.')
        if ep.get("doc"):
            lines.append(f"    Vendor docs: https://api.shinemonitor.com/{ep['doc']}")
        lines.append('    """')
        lines.extend(body)

        lines.append("")
        lines.append(f"def parse_{snake}(payload: dict[str, Any]) -> dict[str, Any]:")
        lines.append(
            f'    """Validate `err` then return the full payload for `{action}`."""'
        )
        lines.append("    return _p.check_response(payload)")
        lines.append("")

    return "\n".join(lines) + "\n"


def render_methods(spec: dict[str, Any]) -> str:
    """Sync + async mixins exposing every generated action as a method."""
    sync_lines = ["class SyncActionsMixin:", '    """GENERATED — do not edit."""', ""]
    async_lines = ["class AsyncActionsMixin:", '    """GENERATED — do not edit."""', ""]
    for ep in spec["endpoints"]:
        action = ep["action"]
        if action in AUTH_ACTIONS:
            continue
        snake = _snake(action)
        params = ep.get("params", [])
        kw_params = [_kw_param(p) for p in params]
        kw_args = [
            f"{p['name'].replace('-', '_')}={p['name'].replace('-', '_')}"
            for p in params
        ]

        sig = "self"
        if kw_params:
            sig += ", *, " + ", ".join(kw_params)
        sync_lines.append(f"    def {snake}({sig}) -> Any:")
        sync_lines.append(
            f'        """Call action `{action}` (chapter {ep.get("chapter", "?")})."""'
        )
        url_call = f"_actions.url_{snake}(self._config, self._require_auth()"
        if kw_args:
            url_call += ", " + ", ".join(kw_args)
        url_call += ")"
        sync_lines.append(f"        url = {url_call}")
        sync_lines.append(f"        return _actions.parse_{snake}(self._get_json(url))")
        sync_lines.append("")

        async_lines.append(f"    async def {snake}({sig}) -> Any:")
        async_lines.append(
            f'        """Call action `{action}` (chapter {ep.get("chapter", "?")})."""'
        )
        async_lines.append(f"        url = {url_call}")
        async_lines.append(
            f"        return _actions.parse_{snake}(await self._get_json(url))"
        )
        async_lines.append("")

    head = [
        '"""GENERATED — do not edit. Run `python scripts/codegen.py`."""',
        "# mypy: disable-error-code=attr-defined",
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "from . import _actions",
        "",
        "",
    ]
    return "\n".join(head + sync_lines + [""] + async_lines) + "\n"


def _kw_param(p: dict[str, Any]) -> str:
    name = p["name"].replace("-", "_")
    py_type = PY_TYPE_MAP.get(p["type"], "str")
    if p.get("required", True):
        return f"{name}: {py_type}"
    return f"{name}: {py_type} | None = None"


def render_mock(spec: dict[str, Any]) -> str:
    handlers: list[tuple[str, str]] = []
    chunks = [
        '"""GENERATED — canned mock responses for documented actions."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any, Callable",
        "",
    ]
    for ep in spec["endpoints"]:
        action = ep["action"]
        if action in AUTH_ACTIONS:
            continue
        snake = _snake(action)
        mock_dat = ep.get("mock_response", _default_dat(action))
        chunks.append("")
        chunks.append(f"def handle_{snake}(params: dict[str, str]) -> dict[str, Any]:")
        chunks.append(f'    """Mock response for `{action}`."""')
        chunks.append(
            f'    return {{"err": 0, "desc": "ERR_NONE", "dat": {mock_dat!r}}}'
        )
        chunks.append("")
        handlers.append((action, snake))

    chunks.append("HANDLERS: dict[str, Callable[[dict[str, str]], dict[str, Any]]] = {")
    for action, snake in handlers:
        chunks.append(f'    "{action}": handle_{snake},')
    chunks.append("}")
    chunks.append("")
    return "\n".join(chunks) + "\n"


def _default_dat(action: str) -> Any:
    if "Count" in action:
        return {"count": 0}
    if "Energy" in action:
        return {"energy": 0.0, "unit": "kWh"}
    if "Power" in action:
        return {"power": 0.0, "unit": "W", "ts": "2026-01-01 00:00:00"}
    if "Status" in action:
        return {"status": 0, "ts": "2026-01-01 00:00:00"}
    if "Plants" in action and action.startswith("query"):
        return {"total": 0, "page": 0, "pagesize": 1, "plant": []}
    if "Collectors" in action and action.startswith("query"):
        return {"total": 0, "page": 0, "pagesize": 1, "collector": []}
    if "Devices" in action and action.startswith("query"):
        return {"total": 0, "page": 0, "pagesize": 1, "device": []}
    return {}


def main() -> None:
    spec = yaml.safe_load(SPEC_FILE.read_text())
    PY_OUT.write_text(render_python(spec))
    PY_METHODS_OUT.write_text(render_methods(spec))
    MOCK_OUT.write_text(render_mock(spec))
    for path in (PY_OUT, PY_METHODS_OUT, MOCK_OUT):
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
