"""GENERATED — canned mock responses for documented actions."""

from __future__ import annotations

from typing import Any, Callable


def handle_update_token(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `updateToken`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_account_info(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryAccountInfo`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_update_password(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `updatePassword`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_plants(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryPlants`."""
    return {
        "err": 0,
        "desc": "ERR_NONE",
        "dat": {"total": 0, "page": 0, "pagesize": 1, "plant": []},
    }


def handle_query_plant_info(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryPlantInfo`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_plant_count(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryPlantCount`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"count": 0}}


def handle_query_plant_energy_day(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryPlantEnergyDay`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"energy": 0.0, "unit": "kWh"}}


def handle_query_plant_energy_month(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryPlantEnergyMonth`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"energy": 0.0, "unit": "kWh"}}


def handle_query_plant_energy_year(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryPlantEnergyYear`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"energy": 0.0, "unit": "kWh"}}


def handle_query_plant_energy_total(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryPlantEnergyTotal`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"energy": 0.0, "unit": "kWh"}}


def handle_query_plant_active_ouput_power_current(
    params: dict[str, str],
) -> dict[str, Any]:
    """Mock response for `queryPlantActiveOuputPowerCurrent`."""
    return {
        "err": 0,
        "desc": "ERR_NONE",
        "dat": {"power": 0.0, "unit": "W", "ts": "2026-01-01 00:00:00"},
    }


def handle_query_collectors(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryCollectors`."""
    return {
        "err": 0,
        "desc": "ERR_NONE",
        "dat": {"total": 0, "page": 0, "pagesize": 1, "collector": []},
    }


def handle_query_collector_info(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryCollectorInfo`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_collector_status(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryCollectorStatus`."""
    return {
        "err": 0,
        "desc": "ERR_NONE",
        "dat": {"status": 0, "ts": "2026-01-01 00:00:00"},
    }


def handle_query_collector_devices(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryCollectorDevices`."""
    return {
        "err": 0,
        "desc": "ERR_NONE",
        "dat": {"total": 0, "page": 0, "pagesize": 1, "device": []},
    }


def handle_query_devices(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDevices`."""
    return {
        "err": 0,
        "desc": "ERR_NONE",
        "dat": {"total": 0, "page": 0, "pagesize": 1, "device": []},
    }


def handle_web_query_device_es(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `webQueryDeviceEs`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_device_count(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceCount`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"count": 0}}


def handle_query_device_info(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceInfo`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_device_last_data(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceLastData`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_sp_device_last_data(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `querySPDeviceLastData`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_device_data_one_day(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceDataOneDay`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_device_status(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceStatus`."""
    return {
        "err": 0,
        "desc": "ERR_NONE",
        "dat": {"status": 0, "ts": "2026-01-01 00:00:00"},
    }


def handle_query_device_warning(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceWarning`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_device_ctrl_field(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceCtrlField`."""
    return {
        "err": 0,
        "desc": "ERR_NONE",
        "dat": {
            "field": [
                {
                    "id": "bse_output_source_priority",
                    "name": "Output source priority",
                    "val": "2",
                    "item": [
                        {"key": "0", "val": "Utility first"},
                        {"key": "1", "val": "Solar first"},
                        {"key": "2", "val": "SBU priority"},
                    ],
                }
            ]
        },
    }


def handle_ctrl_device(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `ctrlDevice`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_query_device_energy_day(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceEnergyDay`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"energy": 0.0, "unit": "kWh"}}


def handle_query_device_energy_month(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceEnergyMonth`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"energy": 0.0, "unit": "kWh"}}


def handle_query_device_energy_year(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceEnergyYear`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"energy": 0.0, "unit": "kWh"}}


def handle_query_device_energy_total(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryDeviceEnergyTotal`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {"energy": 0.0, "unit": "kWh"}}


def handle_query_device_active_ouput_power_current(
    params: dict[str, str],
) -> dict[str, Any]:
    """Mock response for `queryDeviceActiveOuputPowerCurrent`."""
    return {
        "err": 0,
        "desc": "ERR_NONE",
        "dat": {"power": 0.0, "unit": "W", "ts": "2026-01-01 00:00:00"},
    }


def handle_query_camera_info(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `queryCameraInfo`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


def handle_upload_img(params: dict[str, str]) -> dict[str, Any]:
    """Mock response for `uploadImg`."""
    return {"err": 0, "desc": "ERR_NONE", "dat": {}}


HANDLERS: dict[str, Callable[[dict[str, str]], dict[str, Any]]] = {
    "updateToken": handle_update_token,
    "queryAccountInfo": handle_query_account_info,
    "updatePassword": handle_update_password,
    "queryPlants": handle_query_plants,
    "queryPlantInfo": handle_query_plant_info,
    "queryPlantCount": handle_query_plant_count,
    "queryPlantEnergyDay": handle_query_plant_energy_day,
    "queryPlantEnergyMonth": handle_query_plant_energy_month,
    "queryPlantEnergyYear": handle_query_plant_energy_year,
    "queryPlantEnergyTotal": handle_query_plant_energy_total,
    "queryPlantActiveOuputPowerCurrent": handle_query_plant_active_ouput_power_current,
    "queryCollectors": handle_query_collectors,
    "queryCollectorInfo": handle_query_collector_info,
    "queryCollectorStatus": handle_query_collector_status,
    "queryCollectorDevices": handle_query_collector_devices,
    "queryDevices": handle_query_devices,
    "webQueryDeviceEs": handle_web_query_device_es,
    "queryDeviceCount": handle_query_device_count,
    "queryDeviceInfo": handle_query_device_info,
    "queryDeviceLastData": handle_query_device_last_data,
    "querySPDeviceLastData": handle_query_sp_device_last_data,
    "queryDeviceDataOneDay": handle_query_device_data_one_day,
    "queryDeviceStatus": handle_query_device_status,
    "queryDeviceWarning": handle_query_device_warning,
    "queryDeviceCtrlField": handle_query_device_ctrl_field,
    "ctrlDevice": handle_ctrl_device,
    "queryDeviceEnergyDay": handle_query_device_energy_day,
    "queryDeviceEnergyMonth": handle_query_device_energy_month,
    "queryDeviceEnergyYear": handle_query_device_energy_year,
    "queryDeviceEnergyTotal": handle_query_device_energy_total,
    "queryDeviceActiveOuputPowerCurrent": handle_query_device_active_ouput_power_current,
    "queryCameraInfo": handle_query_camera_info,
    "uploadImg": handle_upload_img,
}
