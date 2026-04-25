# shinemonitor-api

Rust client for the ShineMonitor REST API (`api.shinemonitor.com`) —
the cloud backend used by WatchPower, SolarPower, and other vendor
companion apps for Voltronic-derived inverters. Sibling of the
[Python](https://pypi.org/project/shinemonitor-api/) and
[Go](https://pkg.go.dev/github.com/davidsmfreire/shinemonitor-api/go)
clients in the same repo.

```toml
[dependencies]
shinemonitor-api = "0.6"
```

## Usage

```rust
use shinemonitor_api::ShineMonitorAPI;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut api = ShineMonitorAPI::new(
        /* serial_number */ "9620230101001",
        /* wifi_pn       */ "W0001234",
        /* dev_code      */ 2451,
        /* dev_addr      */ 1,
    );

    api.login("user", "pass")?;

    // Generated from spec/endpoints.yaml — every documented vendor
    // action is available as a method on `ShineMonitorAPI`.
    let raw = api.query_account_info()?;
    println!("{raw}");

    // Handwritten parser for the rich `querySPDeviceLastData` payload.
    let snapshot = api.get_last_data()?;
    println!("battery_capacity = {}", snapshot.main.battery_capacity);

    Ok(())
}
```

## Errors

Non-zero `err` codes from the vendor surface as `ApiError`:

```rust
match api.login("user", "wrong") {
    Err(e) if e.is_auth() => {
        // 0x0007 / 0x000F / 0x0010 / 0x0019 / 0x0105 / 0x010E —
        // documented auth-band; re-prompt for credentials.
    }
    Err(e) => eprintln!("err=0x{:04X} desc={}", e.err, e.desc),
    Ok(()) => {}
}
```

## Configuration

```rust
let api = ShineMonitorAPI::new("sn", "pn", 2451, 1)
    .with_base_url("http://your-host/public/")
    .with_suffix_context("&_app_id_=...")
    .with_company_key("...");
```

Defaults pin the request fingerprint to the WatchPower Android app
(reverse-engineered company key + suffix). Override only when targeting
a different vendor app.

## Testing against the mock

Integration tests in `tests/mock.rs` spawn the Python mock server
(`shinemonitor-mock`) as a subprocess. Set `SHINEMONITOR_MOCK_PYTHON`
to a Python interpreter that has the package installed, or run
`uv sync` in `../python/` first.

```sh
cargo test
```

## Repo

[github.com/davidsmfreire/shinemonitor-api](https://github.com/davidsmfreire/shinemonitor-api)
— spec, codegen, mock server, and the Python/Go siblings live there.
