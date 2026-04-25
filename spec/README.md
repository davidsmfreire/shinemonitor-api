# spec

Source of truth for the WatchPower / ShineMonitor API surface. Both
`python/` and `rust/` clients are built against this directory.

## Upstream

Full vendor API reference: https://api.shinemonitor.com/

## Files

- `daily_data_schema.json` — JSON Schema for the `queryDeviceDailyData`
  response payload.

## Adding new endpoints

1. Capture the request/response from `https://api.shinemonitor.com/`.
2. Drop a JSON Schema (or future OpenAPI fragment) in this directory.
3. Wire it into both clients. Co-release version bumps both crates.
