//! Integration test against the language-agnostic mock server.
//!
//! Requires the `shinemonitor-mock` Python package to be importable
//! by some Python interpreter. Resolution order:
//!
//! 1. `SHINEMONITOR_MOCK_PYTHON` env var (absolute path to python).
//! 2. `../python/.venv/bin/python` (created by `uv sync` in python/).
//! 3. Skip with a warning.

use std::env;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::time::{Duration, Instant};

use shinemonitor_api::ShineMonitorAPI;

const FIXTURE_USERNAME: &str = "demo-user";
const FIXTURE_PASSWORD: &str = "demo-pass";
const FIXTURE_COMPANY_KEY: &str = "test-company";
const FIXTURE_SUFFIX: &str = "&source=1&_app_client_=android&_app_id_=test.app&_app_version_=0.0.1";
const FIXTURE_SN: &str = "9620230101001";
const FIXTURE_PN: &str = "W0001234";
const FIXTURE_DEVADDR: i32 = 1;
const FIXTURE_DEVCODE: i32 = 2451;

fn find_python() -> Option<PathBuf> {
    if let Ok(p) = env::var("SHINEMONITOR_MOCK_PYTHON") {
        return Some(PathBuf::from(p));
    }
    // From rust/, the python venv created by `uv sync` in python/. The
    // venv's bin/python symlinks to the underlying interpreter, but we
    // must keep the venv path so its site-packages (which contain
    // shinemonitor_mock) are picked up — symlinks are followed at exec
    // time without losing PYTHONHOME.
    let manifest = env::var("CARGO_MANIFEST_DIR").ok()?;
    let candidate = PathBuf::from(manifest).join("../python/.venv/bin/python");
    if candidate.exists() {
        Some(candidate)
    } else {
        None
    }
}

struct MockServer {
    child: Child,
    url: String,
}

impl MockServer {
    fn spawn(python: &PathBuf) -> Self {
        let mut child = Command::new(python)
            .args(["-m", "shinemonitor_mock", "--port", "0"])
            .env("PYTHONUNBUFFERED", "1")
            .stdout(Stdio::piped())
            .stderr(Stdio::inherit())
            .spawn()
            .expect("failed to spawn shinemonitor_mock");

        let stdout = child.stdout.take().expect("child stdout");
        let mut reader = BufReader::new(stdout);
        let mut line = String::new();
        reader
            .read_line(&mut line)
            .expect("read announcement line from mock");
        let line = line.trim();
        let url = line
            .strip_prefix("LISTENING ")
            .unwrap_or_else(|| panic!("unexpected mock greeting: {line:?}"))
            .trim_end_matches('/')
            .to_string();

        // Wait until the socket actually accepts.
        let deadline = Instant::now() + Duration::from_secs(5);
        let probe = format!("{url}/public/?action=__ping__");
        loop {
            match reqwest::blocking::get(&probe) {
                Ok(_) => break,
                Err(e) if Instant::now() >= deadline => {
                    panic!("mock never accepted: {e}");
                }
                Err(_) => std::thread::sleep(Duration::from_millis(50)),
            }
        }

        MockServer { child, url }
    }
}

impl Drop for MockServer {
    fn drop(&mut self) {
        let _ = self.child.kill();
        let _ = self.child.wait();
    }
}

fn build_api(base_url: &str) -> ShineMonitorAPI {
    ShineMonitorAPI::new(FIXTURE_SN, FIXTURE_PN, FIXTURE_DEVCODE, FIXTURE_DEVADDR)
        .with_base_url(format!("{base_url}/public/"))
        .with_suffix_context(FIXTURE_SUFFIX)
        .with_company_key(FIXTURE_COMPANY_KEY)
}

#[test]
fn login_and_get_last_data() {
    let Some(python) = find_python() else {
        eprintln!("skipping mock test: set SHINEMONITOR_MOCK_PYTHON or run `uv sync` in python/");
        return;
    };

    let server = MockServer::spawn(&python);
    let mut api = build_api(&server.url);

    api.login(FIXTURE_USERNAME, FIXTURE_PASSWORD)
        .expect("login");

    let snapshot = api.get_last_data().expect("get_last_data");
    assert_eq!(snapshot.main.battery_capacity, 85);
    assert_eq!(snapshot.main.ac_output_active_power, 1100);
    assert_eq!(snapshot.system.model, "5KW Inverter");
    assert!((snapshot.main.battery_voltage - 52.4).abs() < 0.001);
}

#[test]
fn login_bad_password_returns_error() {
    let Some(python) = find_python() else {
        eprintln!("skipping mock test: set SHINEMONITOR_MOCK_PYTHON or run `uv sync` in python/");
        return;
    };

    let server = MockServer::spawn(&python);
    let mut api = build_api(&server.url);
    let err = api.login(FIXTURE_USERNAME, "wrong").unwrap_err();
    assert_eq!(err.err, 0x0010);
    assert!(err.is_auth(), "0x0010 must be auth-band");
    assert!(err.desc.contains("ERR_PASSWORD_ERROR"), "got {}", err.desc);
}

#[test]
fn daily_data_returns_payload() {
    let Some(python) = find_python() else {
        eprintln!("skipping");
        return;
    };

    let server = MockServer::spawn(&python);
    let mut api = build_api(&server.url);
    api.login(FIXTURE_USERNAME, FIXTURE_PASSWORD)
        .expect("login");
    let day = chrono::NaiveDate::from_ymd_opt(2026, 4, 25).unwrap();
    let raw = api.get_daily_data(day).expect("daily_data");
    let row_count = raw["dat"]["row"].as_array().map(|a| a.len()).unwrap_or(0);
    assert_eq!(row_count, 2);
}
