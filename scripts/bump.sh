#!/usr/bin/env bash
# Bump python/ and rust/ to the same version, commit, and tag.
# Usage: scripts/bump.sh 0.4.0
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <version>" >&2
  exit 1
fi

VERSION=$1
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

sed -i "s/^version = .*/version = \"$VERSION\"/" "$ROOT/python/pyproject.toml"
sed -i "s/^version = .*/version = \"$VERSION\"/" "$ROOT/rust/Cargo.toml"

(cd "$ROOT/python" && uv lock)
(cd "$ROOT/rust" && cargo update -p shinemonitor-api --precise "$VERSION" 2>/dev/null || cargo generate-lockfile)

git -C "$ROOT" add python/pyproject.toml python/uv.lock rust/Cargo.toml rust/Cargo.lock
git -C "$ROOT" commit -m "release: v$VERSION"
git -C "$ROOT" tag "v$VERSION"

echo "tagged v$VERSION — push with: git push origin main --tags"
