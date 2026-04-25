"""Reusable mock of the ShineMonitor REST API for cross-language tests."""

from __future__ import annotations

from .server import (
    DAILY_DATA_ROWS,
    DAILY_DATA_TITLES,
    DEVICES,
    ISSUED_SECRET,
    ISSUED_TOKEN,
    LAST_DATA_BY_SN,
    TOKEN_EXPIRES,
    VALID_COMPANY_KEY,
    VALID_PASSWORD,
    VALID_USERNAME,
    create_app,
)

__all__ = [
    "DAILY_DATA_ROWS",
    "DAILY_DATA_TITLES",
    "DEVICES",
    "ISSUED_SECRET",
    "ISSUED_TOKEN",
    "LAST_DATA_BY_SN",
    "TOKEN_EXPIRES",
    "VALID_COMPANY_KEY",
    "VALID_PASSWORD",
    "VALID_USERNAME",
    "create_app",
]
