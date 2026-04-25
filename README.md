# watchpower-api

Multi-language clients for the WatchPower / ShineMonitor inverter API
(https://api.shinemonitor.com/).

## Layout

| Path      | What                                           |
| --------- | ---------------------------------------------- |
| `spec/`   | API schemas — source of truth for both clients |
| `python/` | Python client (`watchpower-api` on PyPI)       |
| `rust/`   | Rust client (`watchpower-api` on crates.io)    |

Both clients release in lockstep from a single `vX.Y.Z` git tag.

## Quick start

- Python: see [`python/README.md`](python/README.md)
- Rust: see [`rust/`](rust/) — `cargo add watchpower-api`

## Releasing

Tag `vX.Y.Z` on `main`. CI publishes to PyPI and crates.io and cuts a
GitHub release with the combined changelog.
