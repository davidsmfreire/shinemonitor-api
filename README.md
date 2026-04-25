# shinemonitor-api

Multi-language clients for the ShineMonitor inverter cloud API
(`api.shinemonitor.com`) — used by WatchPower, SolarPower, and other
vendor apps for Voltronic-derived inverters.

## Layout

| Path                 | What                                                                |
| -------------------- | ------------------------------------------------------------------- |
| `spec/`              | Endpoint catalog + schemas — source of truth for every client       |
| `python/`            | Python client (`shinemonitor-api` on PyPI)                          |
| `rust/`              | Rust client (`shinemonitor-api` on crates.io)                       |
| `go/`                | Go client (`github.com/davidsmfreire/shinemonitor-api/go`, via tag) |
| `mock-server/`       | Cross-language mock used by every client test suite                 |
| `scripts/codegen.py` | Reads `spec/endpoints.yaml`, emits client + mock action files       |
| `custom_components/` | Home Assistant integration (HACS-installable)                       |

Python and Rust release in lockstep from a single `vX.Y.Z` git tag. Go
uses a separate `go/vX.Y.Z` tag (Go module proxy requires the path
prefix); both tags ship from the same commit.

## Quick start

- Python: see [`python/README.md`](python/README.md) —
  `pip install shinemonitor-api`
- Rust: see [`rust/`](rust/) — `cargo add shinemonitor-api`
- Go: see [`go/README.md`](go/README.md) —
  `go get github.com/davidsmfreire/shinemonitor-api/go`
- Home Assistant: add this repo as a HACS custom repository (type:
  _Integration_) and install **ShineMonitor**. See
  [`info.md`](info.md).

## Releasing

1. `bash scripts/bump.sh X.Y.Z` — bumps `python/pyproject.toml` and
   `rust/Cargo.toml`, commits, and tags `vX.Y.Z`.
2. `git tag go/vX.Y.Z` on the same commit.
3. `git push origin main --tags`.

CI publishes the Python tag to PyPI and the Rust tag to crates.io, then
cuts a GitHub release with the combined changelog. The Go module proxy
picks up `go/vX.Y.Z` automatically — no publish step.

## Adding endpoints

Edit `spec/endpoints.yaml` and run `python scripts/codegen.py`. That
regenerates the URL builders, methods, and mock handlers for every
client. Auth flows (`auth`, `authSource`) stay handwritten because they
sign differently. See [`spec/README.md`](spec/README.md).

## Renamed from `watchpower-api`

This project was renamed because the API serves multiple apps, not
only WatchPower. Old PyPI/crates.io packages remain published as
`watchpower-api` up to `0.3.0` (Python) and `0.0.5` (Rust); new
releases ship as `shinemonitor-api`.
