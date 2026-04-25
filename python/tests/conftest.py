"""Pytest fixtures: spawn the cross-language mock server as a subprocess.

We deliberately use the subprocess path that Rust and other-language
suites will use, so the fixture exercises the same `python -m
shinemonitor_mock` boundary the others do. Session-scoped to amortize
the ~half-second uvicorn startup.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from collections.abc import AsyncIterator, Iterator

import httpx
import pytest


@pytest.fixture(scope="session")
def mock_url() -> Iterator[str]:
    proc = subprocess.Popen(
        [sys.executable, "-m", "shinemonitor_mock", "--port", "0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )
    try:
        assert proc.stdout is not None
        line = proc.stdout.readline().strip()
        if not line.startswith("LISTENING "):
            raise RuntimeError(f"mock did not announce: {line!r}")
        url = line.removeprefix("LISTENING ").rstrip("/")
        # Wait for the socket to actually accept.
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            try:
                httpx.get(url + "/public/?action=__ping__", timeout=0.5)
                break
            except httpx.HTTPError:
                time.sleep(0.05)
        else:
            raise RuntimeError("mock never accepted connections")
        yield url
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.fixture
def base_url(mock_url: str) -> str:
    return f"{mock_url}/public/"


@pytest.fixture
def sync_http() -> Iterator[httpx.Client]:
    with httpx.Client(timeout=5.0) as client:
        yield client


@pytest.fixture
async def async_http() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        yield client


@pytest.fixture
def client_kwargs(base_url: str) -> dict[str, str]:
    return {
        "base_url": base_url,
        "company_key": "test-company",
        "suffix_context": (
            "&source=1&_app_client_=android&_app_id_=test.app&_app_version_=0.0.1"
        ),
    }
