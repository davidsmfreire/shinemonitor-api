use chrono::{NaiveDate, NaiveDateTime};
use reqwest::blocking::Client;
use serde::Serialize;
use sha1::{Digest, Sha1};
use std::collections::HashSet;
use std::fmt;
use std::time::{SystemTime, UNIX_EPOCH};

mod actions;

pub type ShineMonitorAPIResult = Result<serde_json::Value, ApiError>;

/// Documented auth-band error codes from chapter 2 (auth.html). Hex in
/// docs, integers on the wire. Mirrors the python and Go clients.
fn auth_err_codes() -> HashSet<i64> {
    [0x0007, 0x000F, 0x0010, 0x0019, 0x0105, 0x010E]
        .into_iter()
        .collect()
}

/// Structured API error mirroring the python `ShineMonitorError` and Go
/// `APIError`. `err == 0` is success and never produces this; non-zero
/// `err` codes raise.
#[derive(Debug, Clone)]
pub struct ApiError {
    pub err: i64,
    pub desc: String,
    pub payload: serde_json::Value,
}

impl ApiError {
    pub fn is_auth(&self) -> bool {
        auth_err_codes().contains(&self.err)
    }

    fn from_payload(payload: serde_json::Value) -> Self {
        let err = payload.get("err").and_then(|v| v.as_i64()).unwrap_or(-1);
        let desc = payload
            .get("desc")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_string();
        ApiError { err, desc, payload }
    }

    fn local(err: i64, desc: impl Into<String>) -> Self {
        ApiError {
            err,
            desc: desc.into(),
            payload: serde_json::Value::Null,
        }
    }
}

impl fmt::Display for ApiError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "shinemonitor: err=0x{:04X} desc={:?}",
            self.err, self.desc
        )
    }
}

impl std::error::Error for ApiError {}

impl From<reqwest::Error> for ApiError {
    fn from(e: reqwest::Error) -> Self {
        ApiError::local(-1, format!("transport: {e}"))
    }
}

#[derive(Debug, Serialize, Clone)]
struct ShineMonitorDeviceParams {
    serial_number: String,
    wifi_pn: String,
    dev_code: i32,
    dev_addr: i32,
}

#[derive(Debug, Serialize, Clone)]
pub struct ShineMonitorLastDataGrid {
    pub grid_rating_voltage: f32,
    pub grid_rating_current: f32,
    pub battery_rating_voltage: f32,
    pub ac_output_rating_voltage: f32,
    pub ac_output_rating_current: f32,
    pub ac_output_rating_frequency: f32,
    pub ac_output_rating_apparent_power: i32,
    pub ac_output_rating_active_power: i32,
}

impl ShineMonitorLastDataGrid {
    fn from_json(json: &serde_json::Value) -> Self {
        let mut grid_rating_voltage = None;
        let mut grid_rating_current = None;
        let mut battery_rating_voltage = None;
        let mut ac_output_rating_voltage = None;
        let mut ac_output_rating_current = None;
        let mut ac_output_rating_frequency = None;
        let mut ac_output_rating_apparent_power = None;
        let mut ac_output_rating_active_power = None;

        for field in json.as_array().unwrap() {
            match field["id"].as_str().unwrap() {
                "gd_grid_rating_voltage" => {
                    grid_rating_voltage =
                        Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "gd_grid_rating_current" => {
                    grid_rating_current =
                        Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "gd_battery_rating_voltage" => {
                    battery_rating_voltage =
                        Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "gd_bse_input_voltage_read" => {
                    ac_output_rating_voltage =
                        Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "gd_ac_output_rating_current" => {
                    ac_output_rating_current =
                        Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "gd_bse_output_frequency_read" => {
                    ac_output_rating_frequency =
                        Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "gd_ac_output_rating_apparent_power" => {
                    ac_output_rating_apparent_power =
                        Some(field["val"].as_str().unwrap().parse::<i32>().unwrap())
                }
                "gd_ac_output_rating_active_power" => {
                    ac_output_rating_active_power =
                        Some(field["val"].as_str().unwrap().parse::<i32>().unwrap())
                }
                _ => continue,
            }
        }
        ShineMonitorLastDataGrid {
            grid_rating_voltage: grid_rating_voltage.expect("Grid rating voltage not found"),
            grid_rating_current: grid_rating_current.expect("Grid rating current not found"),
            battery_rating_voltage: battery_rating_voltage
                .expect("Battery rating voltage not found"),
            ac_output_rating_voltage: ac_output_rating_voltage
                .expect("AC output rating voltage not found"),
            ac_output_rating_current: ac_output_rating_current
                .expect("AC output rating current not found"),
            ac_output_rating_frequency: ac_output_rating_frequency
                .expect("AC output rating frequency not found"),
            ac_output_rating_apparent_power: ac_output_rating_apparent_power
                .expect("AC output rating apparent power not found"),
            ac_output_rating_active_power: ac_output_rating_active_power
                .expect("AC output rating active power not found"),
        }
    }
}

#[derive(Debug, Serialize, Clone)]
pub struct ShineMonitorLastDataSystem {
    pub model: String,
    pub main_cpu_firmware_version: String,
    pub secondary_cpu_firmware_version: String,
}

impl ShineMonitorLastDataSystem {
    fn from_json(json: &serde_json::Value) -> Self {
        let mut model = None;
        let mut main_cpu_firmware_version = None;
        let mut secondary_cpu_firmware_version = None;

        for field in json.as_array().unwrap() {
            match field["id"].as_str().unwrap() {
                "sy_model" => model = Some(field["val"].as_str().unwrap().to_owned()),
                "sy_main_cpu1_firmware_version" => {
                    main_cpu_firmware_version = Some(field["val"].as_str().unwrap().to_owned())
                }
                "sy_main_cpu2_firmware_version" => {
                    secondary_cpu_firmware_version = Some(field["val"].as_str().unwrap().to_owned())
                }
                _ => continue,
            }
        }
        ShineMonitorLastDataSystem {
            model: model.expect("Model not found"),
            main_cpu_firmware_version: main_cpu_firmware_version
                .expect("Main CPU firmware version not found"),
            secondary_cpu_firmware_version: secondary_cpu_firmware_version
                .expect("Secondary CPU firmware version not found"),
        }
    }
}

#[derive(Debug, Serialize, Clone)]
pub struct ShineMonitorLastDataPV {
    pub pv_input_current: f32,
}

impl ShineMonitorLastDataPV {
    fn from_json(json: &serde_json::Value) -> Self {
        let mut pv_input_current = None;
        for field in json.as_array().unwrap() {
            match field["id"].as_str().unwrap() {
                "pv_input_current" => {
                    pv_input_current = Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                _ => continue,
            }
        }
        ShineMonitorLastDataPV {
            pv_input_current: pv_input_current.expect("PV input current not found"),
        }
    }
}

#[derive(Debug, Serialize, Clone)]
pub struct ShineMonitorLastDataMain {
    pub grid_voltage: f32,
    pub grid_frequency: f32,
    pub pv_input_voltage: f32,
    pub pv_input_power: i16,
    pub battery_voltage: f32,
    pub battery_capacity: i8,
    pub battery_charging_current: f32,
    pub battery_discharge_current: f32,
    pub ac_output_voltage: f32,
    pub ac_output_frequency: f32,
    pub ac_output_apparent_power: i32,
    pub ac_output_active_power: i32,
    pub output_load_percent: i8,
}

impl ShineMonitorLastDataMain {
    fn from_json(json: &serde_json::Value) -> Self {
        let mut grid_voltage = None;
        let mut grid_frequency = None;
        let mut pv_input_voltage = None;
        let mut pv_input_power = None;
        let mut battery_voltage = None;
        let mut battery_capacity = None;
        let mut battery_charging_current = None;
        let mut battery_discharge_current = None;
        let mut ac_output_voltage = None;
        let mut ac_output_frequency = None;
        let mut ac_output_apparent_power = None;
        let mut ac_output_active_power = None;
        let mut output_load_percent = None;
        for field in json.as_array().unwrap() {
            match field["id"].as_str().unwrap() {
                "bt_grid_voltage" => {
                    grid_voltage = Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "bt_grid_frequency" => {
                    grid_frequency = Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "bt_voltage_1" => {
                    pv_input_voltage = Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "bt_input_power" => {
                    pv_input_power = Some(field["val"].as_str().unwrap().parse::<i16>().unwrap())
                }
                "bt_battery_voltage" => {
                    battery_voltage = Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "bt_battery_capacity" => {
                    battery_capacity = Some(field["val"].as_str().unwrap().parse::<i8>().unwrap())
                }
                "bt_battery_charging_current" => {
                    battery_charging_current =
                        Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "bt_battery_discharge_current" => {
                    battery_discharge_current =
                        Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "bt_ac_output_voltage" => {
                    ac_output_voltage = Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "bt_grid_AC_frequency" => {
                    ac_output_frequency =
                        Some(field["val"].as_str().unwrap().parse::<f32>().unwrap())
                }
                "bt_ac_output_apparent_power" => {
                    ac_output_apparent_power =
                        Some(field["val"].as_str().unwrap().parse::<i32>().unwrap())
                }
                "bt_load_active_power_sole" => {
                    ac_output_active_power =
                        Some(field["val"].as_str().unwrap().parse::<i32>().unwrap())
                }
                "bt_output_load_percent" => {
                    output_load_percent =
                        Some(field["val"].as_str().unwrap().parse::<i8>().unwrap())
                }
                _ => continue,
            }
        }
        ShineMonitorLastDataMain {
            grid_voltage: grid_voltage.expect("Grid voltage not found"),
            grid_frequency: grid_frequency.expect("Grid frequency not found"),
            pv_input_voltage: pv_input_voltage.expect("PV input voltage not found"),
            pv_input_power: pv_input_power.expect("PV input power not found"),
            battery_voltage: battery_voltage.expect("Battery voltage not found"),
            battery_capacity: battery_capacity.expect("Battery capacity not found"),
            battery_charging_current: battery_charging_current
                .expect("Battery charging current not found"),
            battery_discharge_current: battery_discharge_current
                .expect("Battery discharge current not found"),
            ac_output_voltage: ac_output_voltage.expect("AC output voltage not found"),
            ac_output_frequency: ac_output_frequency.expect("AC output frequency not found"),
            ac_output_apparent_power: ac_output_apparent_power
                .expect("AC output apparent power not found"),
            ac_output_active_power: ac_output_active_power
                .expect("AC output active power not found"),
            output_load_percent: output_load_percent.expect("Output load percent not found"),
        }
    }
}

#[derive(Debug, Serialize, Clone)]
pub struct ShineMonitorLastData {
    pub timestamp: NaiveDateTime,
    pub grid: ShineMonitorLastDataGrid,
    pub system: ShineMonitorLastDataSystem,
    pub pv: ShineMonitorLastDataPV,
    pub main: ShineMonitorLastDataMain,
}

impl ShineMonitorLastData {
    fn from_json(json: &serde_json::Value) -> Self {
        let dat_field = &json["dat"];
        let pars_field = &dat_field["pars"];
        ShineMonitorLastData {
            timestamp: parse_gts(&dat_field["gts"]),
            grid: ShineMonitorLastDataGrid::from_json(&pars_field["gd_"]),
            system: ShineMonitorLastDataSystem::from_json(&pars_field["sy_"]),
            pv: ShineMonitorLastDataPV::from_json(&pars_field["pv_"]),
            main: ShineMonitorLastDataMain::from_json(&pars_field["bt_"]),
        }
    }
}

/// Parse `gts` which the vendor returns either as
/// "yyyy-mm-dd HH:MM:SS" or as a milliseconds-since-epoch string.
fn parse_gts(value: &serde_json::Value) -> NaiveDateTime {
    if let Some(raw) = value.as_str() {
        let trimmed = raw.trim();
        if let Ok(ms) = trimmed.parse::<i64>() {
            return chrono::DateTime::from_timestamp_millis(ms)
                .expect("valid epoch ms")
                .naive_utc();
        }
        return NaiveDateTime::parse_from_str(trimmed, "%Y-%m-%d %H:%M:%S")
            .expect("valid gts string");
    }
    if let Some(ms) = value.as_i64() {
        return chrono::DateTime::from_timestamp_millis(ms)
            .expect("valid epoch ms")
            .naive_utc();
    }
    panic!("unexpected gts value: {value:?}");
}

#[derive(Debug, Clone)]
pub struct ShineMonitorAPI {
    _base_url: String,
    _suffix_context: String,
    _company_key: String,
    _token: Option<String>,
    _secret: String,
    _expire: Option<u64>,
    _client: Client,
    _device_params: ShineMonitorDeviceParams,
}

impl ShineMonitorAPI {
    pub fn new(serial_number: &str, wifi_pn: &str, dev_code: i32, dev_addr: i32) -> Self {
        ShineMonitorAPI {
            _base_url: "http://android.shinemonitor.com/public/".to_string(),
            _suffix_context: "&i18n=pt_BR&lang=pt_BR&source=1&_app_client_=android&_app_id_=wifiapp.volfw.watchpower&_app_version_=1.0.6.3".to_string(),
            _company_key: "bnrl_frRFjEz8Mkn".to_string(),
            _token: None,
            _secret: "ems_secret".to_string(),
            _expire: None,
            _client: Client::new(),
            _device_params: ShineMonitorDeviceParams {
                serial_number: serial_number.to_string(),
                wifi_pn: wifi_pn.to_string(),
                dev_code,
                dev_addr,
            },
        }
    }

    pub fn with_base_url(mut self, base_url: impl Into<String>) -> Self {
        self._base_url = base_url.into();
        self
    }

    pub fn with_suffix_context(mut self, suffix: impl Into<String>) -> Self {
        self._suffix_context = suffix.into();
        self
    }

    pub fn with_company_key(mut self, key: impl Into<String>) -> Self {
        self._company_key = key.into();
        self
    }

    fn generate_salt() -> String {
        let start = SystemTime::now();
        let since_the_epoch = start
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards");
        (since_the_epoch.as_millis()).to_string()
    }

    fn sha1_str_lower_case(input: &[u8]) -> String {
        let mut hasher = Sha1::new();
        hasher.update(input);
        format!("{:x}", hasher.finalize())
    }

    fn hash(&self, args: Vec<&str>) -> String {
        let arg_concat = args.join("");
        ShineMonitorAPI::sha1_str_lower_case(arg_concat.as_bytes())
    }

    pub fn login(&mut self, username: &str, password: &str) -> Result<(), ApiError> {
        let base_action = format!(
            "&action=authSource&usr={}&company-key={}{}",
            username, self._company_key, self._suffix_context
        );

        let salt = ShineMonitorAPI::generate_salt();
        let password_hash = self.hash(vec![password]);
        let sign = self.hash(vec![&salt, &password_hash, &base_action]);

        let url = format!(
            "{}?sign={}&salt={}{}",
            self._base_url, sign, salt, base_action
        );

        let response: serde_json::Value = self._client.get(&url).send()?.json()?;

        if response["err"].as_i64() == Some(0) {
            self._secret = response["dat"]["secret"].as_str().unwrap().to_string();
            self._token = Some(response["dat"]["token"].as_str().unwrap().to_string());
            self._expire = Some(response["dat"]["expire"].as_u64().unwrap());
            Ok(())
        } else {
            Err(ApiError::from_payload(response))
        }
    }

    fn _request(&self, action: &str, query: Option<&str>) -> ShineMonitorAPIResult {
        let base_action = format!(
            "&action={}&pn={}&devcode={}&sn={}&devaddr={}{}{}",
            action,
            self._device_params.wifi_pn,
            self._device_params.dev_code,
            self._device_params.serial_number,
            self._device_params.dev_addr,
            query.unwrap_or(""),
            self._suffix_context
        );
        self._request_raw(&base_action)
    }

    /// Sign and dispatch a request whose `base_action` was assembled by the
    /// caller. The generated action methods in `actions.rs` use this so they
    /// don't have to drag the legacy device-params into every call.
    pub fn _request_with(&self, action: &str, extra: &str) -> ShineMonitorAPIResult {
        let base_action = format!("&action={}{}{}", action, extra, self._suffix_context);
        self._request_raw(&base_action)
    }

    fn _request_raw(&self, base_action: &str) -> ShineMonitorAPIResult {
        let token = self
            ._token
            .as_ref()
            .ok_or_else(|| ApiError::local(-1, "not logged in"))?;
        let salt = ShineMonitorAPI::generate_salt();
        let sign = self.hash(vec![&salt, &self._secret, token, base_action]);
        let auth = format!("?sign={}&salt={}&token={}", sign, salt, token);
        let url = format!("{}{}{}", self._base_url, auth, base_action);

        let response: serde_json::Value = self._client.get(&url).send()?.json()?;

        if response["err"].as_i64() == Some(0) {
            Ok(response)
        } else {
            Err(ApiError::from_payload(response))
        }
    }

    pub fn get_daily_data(&self, day: NaiveDate) -> Result<serde_json::Value, ApiError> {
        let _date = day.format("%Y-%m-%d").to_string();
        let query = format!("&date={}", _date);
        self._request("queryDeviceDataOneDay", Some(&query))
    }

    pub fn get_last_data(&self) -> Result<ShineMonitorLastData, ApiError> {
        let raw = self._request("querySPDeviceLastData", None)?;
        Ok(ShineMonitorLastData::from_json(&raw))
    }
}
