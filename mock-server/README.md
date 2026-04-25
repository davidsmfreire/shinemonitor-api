# shinemonitor-mock

In-process and subprocess-friendly mock of the ShineMonitor REST API.
Used by both the Python and Rust client test suites; usable as-is from
any language that can spawn a subprocess and parse one line of stdout.

## Usage

### From any language — subprocess

```sh
python -m shinemonitor_mock --port 0
```

Prints exactly one line to stdout before serving:

```
LISTENING http://127.0.0.1:54321/
```

Tests should read that line, point the client under test at the URL,
and tear the process down at the end of the suite.

### From Python — in-process

```python
from shinemonitor_mock import create_app
import httpx

transport = httpx.ASGITransport(app=create_app())
with httpx.Client(transport=transport, base_url="http://mock") as client:
    ...
```

## Fixture data

Importable constants live alongside the server: `VALID_USERNAME`,
`VALID_PASSWORD`, `VALID_COMPANY_KEY`, `ISSUED_TOKEN`, `ISSUED_SECRET`,
`DEVICES`, `LAST_DATA_BY_SN`, `DAILY_DATA_ROWS`, `DAILY_DATA_TITLES`.
