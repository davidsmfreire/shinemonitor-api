## Feature Parity Rule

All features and bug fixes **must** be implemented in **all three client
languages** (Python, Rust, Go) before a release is cut. No single-language
changes are permitted unless the feature is inherently language-specific
(e.g. the Home Assistant `custom_components/` which is Python-only).

**Rationale:** the three clients share the same API surface and serve the
same user base. Leaving one behind creates confusion and support burden.

## Version Bump Procedure

When preparing a release:

1. Bump version in `python/pyproject.toml` (drives build)
2. Bump version in `python/shinemonitor_api/__init__.py` (`__version__`)
3. Run `uv lock` in `python/` to update lockfile
4. Bump version in `rust/Cargo.toml`
5. Run `cargo generate-lockfile` in `rust/` to update `Cargo.lock`
6. Commit as `chore: bump version to X.Y.Z` (include `Cargo.lock`)
7. Push to main
8. Delete old tag: `git tag -d vX.Y.Z && git push --delete origin vX.Y.Z`
9. Create new tag: `git tag vX.Y.Z && git push origin vX.Y.Z`

The tag push triggers the release workflow which publishes to PyPI, crates.io,
and creates a GitHub release. The Go client does not carry a separate version
field — it relies on module tags (`go/vX.Y.Z`).
