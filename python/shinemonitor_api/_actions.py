"""GENERATED — do not edit. Run `python scripts/codegen.py`."""

from __future__ import annotations

from typing import Any

from . import _protocol as _p


def url_update_token(config: _p.ProtocolConfig, auth: _p.AuthState) -> str:
    """Action `updateToken` — chapter 2.
    Vendor docs: https://api.shinemonitor.com/chapter2/updateToken.html
    """
    base_action = f"&action=updateToken{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_update_token(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `updateToken`."""
    return _p.check_response(payload)


def url_query_account_info(config: _p.ProtocolConfig, auth: _p.AuthState) -> str:
    """Action `queryAccountInfo` — chapter 2.
    Vendor docs: https://api.shinemonitor.com/chapter2/queryAccountInfo.html
    """
    base_action = f"&action=queryAccountInfo{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_account_info(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryAccountInfo`."""
    return _p.check_response(payload)


def url_update_password(
    config: _p.ProtocolConfig, auth: _p.AuthState, oldPwd: str, newPwd: str
) -> str:
    """Action `updatePassword` — chapter 2.
    Vendor docs: https://api.shinemonitor.com/chapter2/updatePassword.html
    """
    base_action = (
        f"&action=updatePassword&oldPwd={oldPwd}&newPwd={newPwd}{config.suffix_context}"
    )
    return _p.authed_url(config, auth, base_action)


def parse_update_password(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `updatePassword`."""
    return _p.check_response(payload)


def url_query_plants(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    status: int | None = None,
    orderBy: str | None = None,
    plantName: str | None = None,
    page: int | None = None,
    pagesize: int | None = None,
) -> str:
    """Action `queryPlants` — chapter 3.
    Vendor docs: https://api.shinemonitor.com/chapter3/queryPlants.html
    """
    base_action = f"&action=queryPlants{config.suffix_context}"
    if status is not None:
        base_action += f"&status={status}"
    if orderBy is not None:
        base_action += f"&orderBy={orderBy}"
    if plantName is not None:
        base_action += f"&plantName={plantName}"
    if page is not None:
        base_action += f"&page={page}"
    if pagesize is not None:
        base_action += f"&pagesize={pagesize}"
    return _p.authed_url(config, auth, base_action)


def parse_query_plants(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryPlants`."""
    return _p.check_response(payload)


def url_query_plant_info(
    config: _p.ProtocolConfig, auth: _p.AuthState, plantid: int
) -> str:
    """Action `queryPlantInfo` — chapter 3.
    Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantInfo.html
    """
    base_action = f"&action=queryPlantInfo&plantid={plantid}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_plant_info(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryPlantInfo`."""
    return _p.check_response(payload)


def url_query_plant_count(config: _p.ProtocolConfig, auth: _p.AuthState) -> str:
    """Action `queryPlantCount` — chapter 3.
    Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantCount.html
    """
    base_action = f"&action=queryPlantCount{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_plant_count(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryPlantCount`."""
    return _p.check_response(payload)


def url_query_plant_energy_day(
    config: _p.ProtocolConfig, auth: _p.AuthState, plantid: int, date: str
) -> str:
    """Action `queryPlantEnergyDay` — chapter 3.
    Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantEnergyDay.html
    """
    base_action = f"&action=queryPlantEnergyDay&plantid={plantid}&date={date}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_plant_energy_day(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryPlantEnergyDay`."""
    return _p.check_response(payload)


def url_query_plant_energy_month(
    config: _p.ProtocolConfig, auth: _p.AuthState, plantid: int, date: str
) -> str:
    """Action `queryPlantEnergyMonth` — chapter 3.
    Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantEnergyMonth.html
    """
    base_action = f"&action=queryPlantEnergyMonth&plantid={plantid}&date={date}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_plant_energy_month(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryPlantEnergyMonth`."""
    return _p.check_response(payload)


def url_query_plant_energy_year(
    config: _p.ProtocolConfig, auth: _p.AuthState, plantid: int, date: str
) -> str:
    """Action `queryPlantEnergyYear` — chapter 3.
    Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantEnergyYear.html
    """
    base_action = f"&action=queryPlantEnergyYear&plantid={plantid}&date={date}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_plant_energy_year(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryPlantEnergyYear`."""
    return _p.check_response(payload)


def url_query_plant_energy_total(
    config: _p.ProtocolConfig, auth: _p.AuthState, plantid: int
) -> str:
    """Action `queryPlantEnergyTotal` — chapter 3.
    Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantEnergyTotal.html
    """
    base_action = (
        f"&action=queryPlantEnergyTotal&plantid={plantid}{config.suffix_context}"
    )
    return _p.authed_url(config, auth, base_action)


def parse_query_plant_energy_total(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryPlantEnergyTotal`."""
    return _p.check_response(payload)


def url_query_plant_active_ouput_power_current(
    config: _p.ProtocolConfig, auth: _p.AuthState, plantid: int
) -> str:
    """Action `queryPlantActiveOuputPowerCurrent` — chapter 3.
    Vendor docs: https://api.shinemonitor.com/chapter3/queryPlantActiveOuputPowerCurrent.html
    """
    base_action = f"&action=queryPlantActiveOuputPowerCurrent&plantid={plantid}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_plant_active_ouput_power_current(
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryPlantActiveOuputPowerCurrent`."""
    return _p.check_response(payload)


def url_query_collectors(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    page: int | None = None,
    pagesize: int | None = None,
) -> str:
    """Action `queryCollectors` — chapter 4.
    Vendor docs: https://api.shinemonitor.com/chapter4/queryCollectors.html
    """
    base_action = f"&action=queryCollectors{config.suffix_context}"
    if page is not None:
        base_action += f"&page={page}"
    if pagesize is not None:
        base_action += f"&pagesize={pagesize}"
    return _p.authed_url(config, auth, base_action)


def parse_query_collectors(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryCollectors`."""
    return _p.check_response(payload)


def url_query_collector_info(
    config: _p.ProtocolConfig, auth: _p.AuthState, pn: str
) -> str:
    """Action `queryCollectorInfo` — chapter 4.
    Vendor docs: https://api.shinemonitor.com/chapter4/queryCollectorInfo.html
    """
    base_action = f"&action=queryCollectorInfo&pn={pn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_collector_info(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryCollectorInfo`."""
    return _p.check_response(payload)


def url_query_collector_status(
    config: _p.ProtocolConfig, auth: _p.AuthState, pn: str
) -> str:
    """Action `queryCollectorStatus` — chapter 4.
    Vendor docs: https://api.shinemonitor.com/chapter4/queryCollectorStatus.html
    """
    base_action = f"&action=queryCollectorStatus&pn={pn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_collector_status(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryCollectorStatus`."""
    return _p.check_response(payload)


def url_query_collector_devices(
    config: _p.ProtocolConfig, auth: _p.AuthState, pn: str
) -> str:
    """Action `queryCollectorDevices` — chapter 4.
    Vendor docs: https://api.shinemonitor.com/chapter4/queryCollectorDevices.html
    """
    base_action = f"&action=queryCollectorDevices&pn={pn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_collector_devices(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryCollectorDevices`."""
    return _p.check_response(payload)


def url_query_devices(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    page: int | None = None,
    pagesize: int | None = None,
) -> str:
    """Action `queryDevices` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/queryDevices.html
    """
    base_action = f"&action=queryDevices{config.suffix_context}"
    if page is not None:
        base_action += f"&page={page}"
    if pagesize is not None:
        base_action += f"&pagesize={pagesize}"
    return _p.authed_url(config, auth, base_action)


def parse_query_devices(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDevices`."""
    return _p.check_response(payload)


def url_web_query_device_es(config: _p.ProtocolConfig, auth: _p.AuthState) -> str:
    """Action `webQueryDeviceEs` — chapter 5."""
    base_action = f"&action=webQueryDeviceEs{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_web_query_device_es(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `webQueryDeviceEs`."""
    return _p.check_response(payload)


def url_query_device_count(config: _p.ProtocolConfig, auth: _p.AuthState) -> str:
    """Action `queryDeviceCount` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceCount.html
    """
    base_action = f"&action=queryDeviceCount{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_count(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceCount`."""
    return _p.check_response(payload)


def url_query_device_info(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
) -> str:
    """Action `queryDeviceInfo` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceInfo.html
    """
    base_action = f"&action=queryDeviceInfo&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_info(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceInfo`."""
    return _p.check_response(payload)


def url_query_device_last_data(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
) -> str:
    """Action `queryDeviceLastData` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceLastData.html
    """
    base_action = f"&action=queryDeviceLastData&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_last_data(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceLastData`."""
    return _p.check_response(payload)


def url_query_sp_device_last_data(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
) -> str:
    """Action `querySPDeviceLastData` — chapter 5."""
    base_action = f"&action=querySPDeviceLastData&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_sp_device_last_data(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `querySPDeviceLastData`."""
    return _p.check_response(payload)


def url_query_device_data_one_day(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
    date: str,
) -> str:
    """Action `queryDeviceDataOneDay` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceDataOneDay.html
    """
    base_action = f"&action=queryDeviceDataOneDay&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}&date={date}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_data_one_day(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceDataOneDay`."""
    return _p.check_response(payload)


def url_query_device_status(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
) -> str:
    """Action `queryDeviceStatus` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceStatus.html
    """
    base_action = f"&action=queryDeviceStatus&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_status(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceStatus`."""
    return _p.check_response(payload)


def url_query_device_warning(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
) -> str:
    """Action `queryDeviceWarning` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceWarning.html
    """
    base_action = f"&action=queryDeviceWarning&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_warning(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceWarning`."""
    return _p.check_response(payload)


def url_query_device_ctrl_field(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
) -> str:
    """Action `queryDeviceCtrlField` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceCtrlField.html
    """
    base_action = f"&action=queryDeviceCtrlField&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_ctrl_field(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceCtrlField`."""
    return _p.check_response(payload)


def url_query_device_ctrl_value(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
) -> str:
    """Action `queryDeviceCtrlValue` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/queryDeviceCtrlValue.html
    """
    base_action = f"&action=queryDeviceCtrlValue&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_ctrl_value(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceCtrlValue`."""
    return _p.check_response(payload)


def url_ctrl_device(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
    id: str,
    val: str,
) -> str:
    """Action `ctrlDevice` — chapter 5.
    Vendor docs: https://api.shinemonitor.com/chapter5/ctrlDevice.html
    """
    base_action = f"&action=ctrlDevice&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}&id={id}&val={val}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_ctrl_device(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `ctrlDevice`."""
    return _p.check_response(payload)


def url_query_device_energy_day(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
    date: str,
) -> str:
    """Action `queryDeviceEnergyDay` — chapter 6.
    Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceEnergyDay.html
    """
    base_action = f"&action=queryDeviceEnergyDay&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}&date={date}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_energy_day(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceEnergyDay`."""
    return _p.check_response(payload)


def url_query_device_energy_month(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
    date: str,
) -> str:
    """Action `queryDeviceEnergyMonth` — chapter 6.
    Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceEnergyMonth.html
    """
    base_action = f"&action=queryDeviceEnergyMonth&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}&date={date}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_energy_month(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceEnergyMonth`."""
    return _p.check_response(payload)


def url_query_device_energy_year(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
    date: str,
) -> str:
    """Action `queryDeviceEnergyYear` — chapter 6.
    Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceEnergyYear.html
    """
    base_action = f"&action=queryDeviceEnergyYear&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}&date={date}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_energy_year(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceEnergyYear`."""
    return _p.check_response(payload)


def url_query_device_energy_total(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
) -> str:
    """Action `queryDeviceEnergyTotal` — chapter 6.
    Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceEnergyTotal.html
    """
    base_action = f"&action=queryDeviceEnergyTotal&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_energy_total(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceEnergyTotal`."""
    return _p.check_response(payload)


def url_query_device_active_ouput_power_current(
    config: _p.ProtocolConfig,
    auth: _p.AuthState,
    pn: str,
    devcode: int,
    devaddr: int,
    sn: str,
) -> str:
    """Action `queryDeviceActiveOuputPowerCurrent` — chapter 6.
    Vendor docs: https://api.shinemonitor.com/chapter6/queryDeviceActiveOuputPowerCurrent.html
    """
    base_action = f"&action=queryDeviceActiveOuputPowerCurrent&pn={pn}&devcode={devcode}&devaddr={devaddr}&sn={sn}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_device_active_ouput_power_current(
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryDeviceActiveOuputPowerCurrent`."""
    return _p.check_response(payload)


def url_query_camera_info(
    config: _p.ProtocolConfig, auth: _p.AuthState, cameraid: int
) -> str:
    """Action `queryCameraInfo` — chapter 11.
    Vendor docs: https://api.shinemonitor.com/chapter11/queryCameraInfo.html
    """
    base_action = f"&action=queryCameraInfo&cameraid={cameraid}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_query_camera_info(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `queryCameraInfo`."""
    return _p.check_response(payload)


def url_upload_img(config: _p.ProtocolConfig, auth: _p.AuthState, fmt: str) -> str:
    """Action `uploadImg` — chapter 84.
    Vendor docs: https://api.shinemonitor.com/chapter84/uploadImg.html
    """
    base_action = f"&action=uploadImg&fmt={fmt}{config.suffix_context}"
    return _p.authed_url(config, auth, base_action)


def parse_upload_img(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate `err` then return the full payload for `uploadImg`."""
    return _p.check_response(payload)
