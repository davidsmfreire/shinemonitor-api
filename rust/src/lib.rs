use chrono::NaiveDate;
use reqwest::blocking::Client;
use sha1::{Digest, Sha1};
use std::time::{SystemTime, UNIX_EPOCH};

type WatchPowerAPIResult = Result<serde_json::Value, Box<dyn std::error::Error>>;

#[derive(Debug)]
struct WatchPowerDailyData {
    // TODO
}

impl WatchPowerDailyData {
    fn from_json(json: &serde_json::Value) -> Self {
        todo!()
    }
}

#[derive(Debug)]
struct WatchPowerDeviceParams {
    serial_number: String,
    wifi_pn: String,
    dev_code: i32,
    dev_addr: i32,
}

#[derive(Debug)]
struct WatchPowerFlowData {
    grid_voltage: f32,
    grid_frequency: f32,
    ac_output_voltage: f32,
    ac_output_active_power: i32,
    output_load_percent: i8,
    battery_capacity: i8,
    battery_voltage: f32,
    pv_input_voltage: f32,
    pv_input_power: f32,
}

impl WatchPowerFlowData {
    fn from_json(json: &serde_json::Value) -> Self {
        todo!()
    }
}

#[derive(Debug)]
pub struct WatchPowerLastDataGrid {
    grid_rating_voltage: f32,
    grid_rating_current: f32,
    battery_rating_voltage: f32,
    ac_output_rating_voltage: f32,
    ac_output_rating_current: f32,
    ac_output_rating_frequency: f32,
    ac_output_rating_apparent_power: i32,
    ac_output_rating_active_power: i32,
}

impl WatchPowerLastDataGrid {
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
        WatchPowerLastDataGrid {
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

#[derive(Debug)]
pub struct WatchPowerLastDataSystem {
    model: String,
    main_cpu_firmware_version: String,
    secondary_cpu_firmware_version: String,
}

impl WatchPowerLastDataSystem {
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
        WatchPowerLastDataSystem {
            model: model.expect("Model not found"),
            main_cpu_firmware_version: main_cpu_firmware_version
                .expect("Main CPU firmware version not found"),
            secondary_cpu_firmware_version: secondary_cpu_firmware_version
                .expect("Secondary CPU firmware version not found"),
        }
    }
}

#[derive(Debug)]
pub struct WatchPowerLastDataPV {
    pv_input_current: f32,
}

impl WatchPowerLastDataPV {
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
        WatchPowerLastDataPV {
            pv_input_current: pv_input_current.expect("PV input current not found"),
        }
    }
}

#[derive(Debug)]
pub struct WatchPowerLastDataMain {
    grid_voltage: f32,
    grid_frequency: f32,
    pv_input_voltage: f32,
    pv_input_power: i16,
    battery_voltage: f32,
    battery_capacity: i8,
    battery_charging_current: f32,
    battery_discharge_current: f32,
    ac_output_voltage: f32,
    ac_output_frequency: f32,
    ac_output_apparent_power: i32,
    ac_output_active_power: i32,
    output_load_percent: i8,
}

impl WatchPowerLastDataMain {
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
        WatchPowerLastDataMain {
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

#[derive(Debug)]
pub struct WatchPowerLastData {
    timestamp: NaiveDate,
    grid: WatchPowerLastDataGrid,
    system: WatchPowerLastDataSystem,
    pv: WatchPowerLastDataPV,
    main: WatchPowerLastDataMain,
}

impl WatchPowerLastData {
    fn from_json(json: &serde_json::Value) -> Self {
        let dat_field = &json["dat"];
        let pars_field = &dat_field["pars"];
        WatchPowerLastData {
            timestamp: NaiveDate::parse_from_str(
                &dat_field["gts"].as_str().unwrap(),
                "%Y-%m-%d %H:%M:%S",
            )
            .unwrap(),
            grid: WatchPowerLastDataGrid::from_json(&pars_field["gd_"]),
            system: WatchPowerLastDataSystem::from_json(&pars_field["sy_"]),
            pv: WatchPowerLastDataPV::from_json(&pars_field["pv_"]),
            main: WatchPowerLastDataMain::from_json(&pars_field["bt_"]),
        }
    }
}

#[derive(Debug)]
pub struct WatchPowerAPI {
    _base_url: String,
    _suffix_context: String,
    _company_key: String,
    _token: Option<String>,
    _secret: String,
    _expire: Option<u64>,
    _client: Client,
    _device_params: WatchPowerDeviceParams,
}

impl WatchPowerAPI {
    pub fn new(serial_number: &str, wifi_pn: &str, dev_code: i32, dev_addr: i32) -> Self {
        WatchPowerAPI {
            _base_url: "http://android.shinemonitor.com/public/".to_string(),
            _suffix_context: "&i18n=pt_BR&lang=pt_BR&source=1&_app_client_=android&_app_id_=wifiapp.volfw.watchpower&_app_version_=1.0.6.3".to_string(),
            _company_key: "bnrl_frRFjEz8Mkn".to_string(),
            _token: None,
            _secret: "ems_secret".to_string(),
            _expire: None,
            _client: Client::new(),
            _device_params: WatchPowerDeviceParams{serial_number: serial_number.to_string(), wifi_pn: wifi_pn.to_string(), dev_code: dev_code, dev_addr: dev_addr},
        }
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
        WatchPowerAPI::sha1_str_lower_case(arg_concat.as_bytes())
    }

    pub fn login(
        &mut self,
        username: &str,
        password: &str,
    ) -> Result<(), Box<dyn std::error::Error>> {
        let base_action = format!(
            "&action=authSource&usr={}&company-key={}{}",
            username, self._company_key, self._suffix_context
        );

        let salt = WatchPowerAPI::generate_salt();
        let password_hash = self.hash(vec![password]);
        let sign = self.hash(vec![&salt, &password_hash, &base_action]);

        let url = format!(
            "{}?sign={}&salt={}{}",
            self._base_url, sign, salt, base_action
        );

        let response: serde_json::Value = self._client.get(&url).send()?.json()?;
        println!("{:?}", response);

        if response["err"].as_u64() == Some(0) {
            self._secret = response["dat"]["secret"].as_str().unwrap().to_string();
            self._token = Some(response["dat"]["token"].as_str().unwrap().to_string());
            self._expire = Some(response["dat"]["expire"].as_u64().unwrap());
            Ok(())
        } else {
            Err(Box::new(std::io::Error::new(
                std::io::ErrorKind::Other,
                format!("Login error: {:?}", response),
            )))
        }
    }

    fn _request(&self, action: &str, query: Option<&str>) -> WatchPowerAPIResult {
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
        let salt = WatchPowerAPI::generate_salt();
        let sign = self.hash(vec![
            &salt,
            &self._secret,
            self._token.as_ref().unwrap(),
            &base_action,
        ]);
        let auth = format!(
            "?sign={}&salt={}&token={}",
            sign,
            salt,
            self._token.as_ref().unwrap()
        );
        let url = format!("{}{}{}", self._base_url, auth, base_action);

        let response: serde_json::Value = self._client.get(&url).send()?.json()?;

        if response["err"] == 0 {
            Ok(response)
        } else {
            Err(Box::new(std::io::Error::new(
                std::io::ErrorKind::Other,
                format!("API error: {:?}", response),
            )))
        }
    }

    fn get_daily_data(
        &self,
        day: NaiveDate,
    ) -> Result<WatchPowerDailyData, Box<dyn std::error::Error>> {
        let _date = day.format("%Y-%m-%d").to_string();
        let query = format!("&date={}", _date);
        match self._request("queryDeviceDataOneDay", Some(&query)) {
            Ok(raw) => Ok(WatchPowerDailyData::from_json(&raw)),
            Err(e) => Err(e),
        }
    }

    fn get_power_flow(&self) -> Result<WatchPowerFlowData, Box<dyn std::error::Error>> {
        match self._request("queryDeviceFlowPower", None) {
            Ok(raw) => Ok(WatchPowerFlowData::from_json(&raw)),
            Err(e) => Err(e),
        }
    }

    pub fn get_last_data(&self) -> Result<WatchPowerLastData, Box<dyn std::error::Error>> {
        match self._request("querySPDeviceLastData", None) {
            Ok(raw) => Ok(WatchPowerLastData::from_json(&raw)),
            Err(e) => Err(e),
        }
    }
}
