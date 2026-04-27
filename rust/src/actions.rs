//! GENERATED — do not edit. Run `python scripts/codegen.py`.
//!
//! Each method drives `ShineMonitorAPI::_request_with` for the
//! corresponding documented vendor action.

#![allow(clippy::too_many_arguments, dead_code)]

use crate::{ApiError, ShineMonitorAPI};

impl ShineMonitorAPI {
    /// Action `updateToken` — chapter 2.
    /// Vendor docs: https://api.shinemonitor.com/chapter2/updateToken.html
    pub fn update_token(&self) -> Result<serde_json::Value, ApiError> {
        let extra = String::new();
        self._request_with("updateToken", &extra)
    }

    /// Action `queryAccountInfo` — chapter 2.
    /// Vendor docs: https://api.shinemonitor.com/chapter2/queryAccountInfo.html
    pub fn query_account_info(&self) -> Result<serde_json::Value, ApiError> {
        let extra = String::new();
        self._request_with("queryAccountInfo", &extra)
    }

    /// Action `updatePassword` — chapter 2.
    /// Vendor docs: https://api.shinemonitor.com/chapter2/updatePassword.html
    pub fn update_password(
        &self,
        old_pwd: &str,
        new_pwd: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&oldPwd={}", old_pwd));
        extra.push_str(&format!("&newPwd={}", new_pwd));
        self._request_with("updatePassword", &extra)
    }

    /// Action `queryPlants` — chapter 3.
    /// Vendor docs: https://api.shinemonitor.com/chapter3/queryPlants.html
    pub fn query_plants(
        &self,
        status: Option<i64>,
        order_by: Option<&str>,
        plant_name: Option<&str>,
        page: Option<i64>,
        pagesize: Option<i64>,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        if let Some(v) = status {
            extra.push_str(&format!("&status={}", v));
        }
        if let Some(v) = order_by {
            extra.push_str(&format!("&orderBy={}", v));
        }
        if let Some(v) = plant_name {
            extra.push_str(&format!("&plantName={}", v));
        }
        if let Some(v) = page {
            extra.push_str(&format!("&page={}", v));
        }
        if let Some(v) = pagesize {
            extra.push_str(&format!("&pagesize={}", v));
        }
        self._request_with("queryPlants", &extra)
    }

    /// Action `queryPlantInfo` — chapter 3.
    /// Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantInfo.html
    pub fn query_plant_info(&self, plantid: i64) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&plantid={}", plantid));
        self._request_with("queryPlantInfo", &extra)
    }

    /// Action `queryPlantCount` — chapter 3.
    /// Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantCount.html
    pub fn query_plant_count(&self) -> Result<serde_json::Value, ApiError> {
        let extra = String::new();
        self._request_with("queryPlantCount", &extra)
    }

    /// Action `queryPlantEnergyDay` — chapter 3.
    /// Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantEnergyDay.html
    pub fn query_plant_energy_day(
        &self,
        plantid: i64,
        date: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&plantid={}", plantid));
        extra.push_str(&format!("&date={}", date));
        self._request_with("queryPlantEnergyDay", &extra)
    }

    /// Action `queryPlantEnergyMonth` — chapter 3.
    /// Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantEnergyMonth.html
    pub fn query_plant_energy_month(
        &self,
        plantid: i64,
        date: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&plantid={}", plantid));
        extra.push_str(&format!("&date={}", date));
        self._request_with("queryPlantEnergyMonth", &extra)
    }

    /// Action `queryPlantEnergyYear` — chapter 3.
    /// Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantEnergyYear.html
    pub fn query_plant_energy_year(
        &self,
        plantid: i64,
        date: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&plantid={}", plantid));
        extra.push_str(&format!("&date={}", date));
        self._request_with("queryPlantEnergyYear", &extra)
    }

    /// Action `queryPlantEnergyTotal` — chapter 3.
    /// Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantEnergyTotal.html
    pub fn query_plant_energy_total(&self, plantid: i64) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&plantid={}", plantid));
        self._request_with("queryPlantEnergyTotal", &extra)
    }

    /// Action `queryPlantActiveOuputPowerCurrent` — chapter 3.
    /// Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantActiveOuputPowerCurrent.html
    pub fn query_plant_active_ouput_power_current(
        &self,
        plantid: i64,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&plantid={}", plantid));
        self._request_with("queryPlantActiveOuputPowerCurrent", &extra)
    }

    /// Action `queryCollectors` — chapter 4.
    /// Vendor docs: https://api.shinemonitor.com/chapter4/queryCollectors.html
    pub fn query_collectors(
        &self,
        page: Option<i64>,
        pagesize: Option<i64>,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        if let Some(v) = page {
            extra.push_str(&format!("&page={}", v));
        }
        if let Some(v) = pagesize {
            extra.push_str(&format!("&pagesize={}", v));
        }
        self._request_with("queryCollectors", &extra)
    }

    /// Action `queryCollectorInfo` — chapter 4.
    /// Vendor docs: https://api.shinemonitor.com/chapter4/queryCollectorInfo.html
    pub fn query_collector_info(&self, pn: &str) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        self._request_with("queryCollectorInfo", &extra)
    }

    /// Action `queryCollectorStatus` — chapter 4.
    /// Vendor docs: https://api.shinemonitor.com/chapter4/queryCollectorStatus.html
    pub fn query_collector_status(&self, pn: &str) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        self._request_with("queryCollectorStatus", &extra)
    }

    /// Action `queryCollectorDevices` — chapter 4.
    /// Vendor docs: https://api.shinemonitor.com/chapter4/queryCollectorDevices.html
    pub fn query_collector_devices(&self, pn: &str) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        self._request_with("queryCollectorDevices", &extra)
    }

    /// Action `queryDevices` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/queryDevices.html
    pub fn query_devices(
        &self,
        page: Option<i64>,
        pagesize: Option<i64>,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        if let Some(v) = page {
            extra.push_str(&format!("&page={}", v));
        }
        if let Some(v) = pagesize {
            extra.push_str(&format!("&pagesize={}", v));
        }
        self._request_with("queryDevices", &extra)
    }

    pub fn web_query_device_es(&self) -> Result<serde_json::Value, ApiError> {
        let extra = String::new();
        self._request_with("webQueryDeviceEs", &extra)
    }

    /// Action `queryDeviceCount` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceCount.html
    pub fn query_device_count(&self) -> Result<serde_json::Value, ApiError> {
        let extra = String::new();
        self._request_with("queryDeviceCount", &extra)
    }

    /// Action `queryDeviceInfo` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceInfo.html
    pub fn query_device_info(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        self._request_with("queryDeviceInfo", &extra)
    }

    /// Action `queryDeviceLastData` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceLastData.html
    pub fn query_device_last_data(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        self._request_with("queryDeviceLastData", &extra)
    }

    pub fn query_sp_device_last_data(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        self._request_with("querySPDeviceLastData", &extra)
    }

    /// Action `queryDeviceDataOneDay` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceDataOneDay.html
    pub fn query_device_data_one_day(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
        date: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        extra.push_str(&format!("&date={}", date));
        self._request_with("queryDeviceDataOneDay", &extra)
    }

    /// Action `queryDeviceStatus` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceStatus.html
    pub fn query_device_status(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        self._request_with("queryDeviceStatus", &extra)
    }

    /// Action `queryDeviceWarning` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceWarning.html
    pub fn query_device_warning(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        self._request_with("queryDeviceWarning", &extra)
    }

    /// Action `queryDeviceCtrlField` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceCtrlField.html
    pub fn query_device_ctrl_field(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        self._request_with("queryDeviceCtrlField", &extra)
    }

    /// Action `queryDeviceCtrlValue` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceCtrlValue.html
    pub fn query_device_ctrl_value(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
        id: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        extra.push_str(&format!("&id={}", id));
        self._request_with("queryDeviceCtrlValue", &extra)
    }

    /// Action `ctrlDevice` — chapter 5.
    /// Vendor docs: https://api.shinemonitor.com/chapter5/ctrlDevice.html
    pub fn ctrl_device(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
        id: &str,
        val: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        extra.push_str(&format!("&id={}", id));
        extra.push_str(&format!("&val={}", val));
        self._request_with("ctrlDevice", &extra)
    }

    /// Action `queryDeviceEnergyDay` — chapter 6.
    /// Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceEnergyDay.html
    pub fn query_device_energy_day(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
        date: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        extra.push_str(&format!("&date={}", date));
        self._request_with("queryDeviceEnergyDay", &extra)
    }

    /// Action `queryDeviceEnergyMonth` — chapter 6.
    /// Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceEnergyMonth.html
    pub fn query_device_energy_month(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
        date: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        extra.push_str(&format!("&date={}", date));
        self._request_with("queryDeviceEnergyMonth", &extra)
    }

    /// Action `queryDeviceEnergyYear` — chapter 6.
    /// Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceEnergyYear.html
    pub fn query_device_energy_year(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
        date: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        extra.push_str(&format!("&date={}", date));
        self._request_with("queryDeviceEnergyYear", &extra)
    }

    /// Action `queryDeviceEnergyTotal` — chapter 6.
    /// Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceEnergyTotal.html
    pub fn query_device_energy_total(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        self._request_with("queryDeviceEnergyTotal", &extra)
    }

    /// Action `queryDeviceActiveOuputPowerCurrent` — chapter 6.
    /// Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceActiveOuputPowerCurrent.html
    pub fn query_device_active_ouput_power_current(
        &self,
        pn: &str,
        devcode: i64,
        devaddr: i64,
        sn: &str,
    ) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&pn={}", pn));
        extra.push_str(&format!("&devcode={}", devcode));
        extra.push_str(&format!("&devaddr={}", devaddr));
        extra.push_str(&format!("&sn={}", sn));
        self._request_with("queryDeviceActiveOuputPowerCurrent", &extra)
    }

    /// Action `queryCameraInfo` — chapter 11.
    /// Vendor docs: https://api.shinemonitor.com/chapter11/queryCameraInfo.html
    pub fn query_camera_info(&self, cameraid: i64) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&cameraid={}", cameraid));
        self._request_with("queryCameraInfo", &extra)
    }

    /// Action `uploadImg` — chapter 84.
    /// Vendor docs: https://api.shinemonitor.com/chapter84/uploadImg.html
    pub fn upload_img(&self, fmt: &str) -> Result<serde_json::Value, ApiError> {
        let mut extra = String::new();
        extra.push_str(&format!("&fmt={}", fmt));
        self._request_with("uploadImg", &extra)
    }
}
