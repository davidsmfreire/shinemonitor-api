# shinemonitor-api

Multi-language clients for the ShineMonitor inverter cloud API
(`api.shinemonitor.com`) — used by WatchPower, SolarPower, and other
vendor apps for Voltronic-derived inverters.

## Layout

| Path      | What                                           |
| --------- | ---------------------------------------------- |
| `spec/`   | API schemas — source of truth for both clients |
| `python/` | Python client (`shinemonitor-api` on PyPI)     |
| `rust/`   | Rust client (`shinemonitor-api` on crates.io)  |

Both clients release in lockstep from a single `vX.Y.Z` git tag.

## Quick start

- Python: see [`python/README.md`](python/README.md)
- Rust: see [`rust/`](rust/) — `cargo add shinemonitor-api`

## Releasing

Tag `vX.Y.Z` on `main`. CI publishes to PyPI and crates.io and cuts a
GitHub release with the combined changelog.

## Renamed from `watchpower-api`

This project was renamed because the API serves multiple apps, not
only WatchPower. Old PyPI/crates.io packages remain published as
`watchpower-api` up to `0.3.0` (Python) and `0.0.5` (Rust); new
releases ship as `shinemonitor-api`.
