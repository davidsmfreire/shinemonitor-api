# spec

Source of truth for the ShineMonitor API surface (used by WatchPower,
SolarPower, and other vendor apps). Every client (`python/`, `rust/`,
`go/`) and the mock server are generated from this directory.

## Upstream

Full vendor API reference: https://api.shinemonitor.com/

## Files

- `endpoints.yaml` — machine-readable catalog of vendor actions: name,
  chapter, params, doc URL, mock response. Drives `scripts/codegen.py`.
- `error_codes.yaml` — vendor `err` codes with descriptions.
- `daily_data_schema.json` — JSON Schema for the `queryDeviceDailyData`
  response payload.

## Adding a new endpoint

1. Capture the request/response from `https://api.shinemonitor.com/`.
2. Append an entry to `endpoints.yaml` (action, chapter, params,
   `mock_response` if non-default).
3. Run `python scripts/codegen.py` from the repo root. That writes:
   - `python/shinemonitor_api/_actions.py` (URL builders + parsers)
   - `python/shinemonitor_api/_methods.py` (sync + async mixins)
   - `rust/src/actions.rs` (impl on `ShineMonitorAPI`)
   - `go/actions.go` (methods on `*Client`, ctx-first)
   - `mock-server/shinemonitor_mock/_actions.py` (canned handlers)
4. Run each client's tests. Bump versions with `scripts/bump.sh` for
   the next release.

Auth actions (`auth`, `authSource`) are skipped by codegen — their
signing scheme differs and they live in handwritten files.
