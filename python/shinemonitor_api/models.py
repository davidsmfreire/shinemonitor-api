from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field
from pydantic.version import VERSION as _PYDANTIC_VERSION

PYDANTIC_VERSION: str = str(_PYDANTIC_VERSION)

if PYDANTIC_VERSION.startswith("2."):
    from pydantic import ConfigDict


class _PopulateByNameMixin(BaseModel):
    if PYDANTIC_VERSION.startswith("2."):
        model_config = ConfigDict(populate_by_name=True)
    else:

        class Config:
            allow_population_by_field_name = True


class DeviceIdentifier(_PopulateByNameMixin):
    device_alias: Optional[str] = Field(default=None, alias="devalias")
    serial_number: str = Field(..., alias="sn")
    wifi_pin: str = Field(..., alias="pn")
    device_address: int = Field(..., alias="devaddr")
    device_code: int = Field(..., alias="devcode")


class LastDataGrid(BaseModel):
    grid_rating_voltage: Optional[float] = None
    grid_rating_current: Optional[float] = None
    battery_rating_voltage: Optional[float] = None
    ac_output_rating_voltage: Optional[float] = None
    ac_output_rating_current: Optional[float] = None
    ac_output_rating_frequency: Optional[float] = None
    ac_output_rating_apparent_power: Optional[int] = None
    ac_output_rating_active_power: Optional[int] = None


class LastDataSystem(BaseModel):
    model: Optional[str] = None
    main_cpu_firmware_version: Optional[str] = None
    secondary_cpu_firmware_version: Optional[str] = None


class LastDataPV(BaseModel):
    pv_input_current: Optional[float] = None


class LastDataMain(BaseModel):
    grid_voltage: Optional[float] = None
    grid_frequency: Optional[float] = None
    pv_input_voltage: Optional[float] = None
    pv_input_power: Optional[int] = None
    battery_voltage: Optional[float] = None
    battery_capacity: Optional[int] = None
    battery_charging_current: Optional[float] = None
    battery_discharge_current: Optional[float] = None
    ac_output_voltage: Optional[float] = None
    ac_output_frequency: Optional[float] = None
    ac_output_apparent_power: Optional[int] = None
    ac_output_active_power: Optional[int] = None
    output_load_percent: Optional[int] = None


class LastData(BaseModel):
    timestamp: datetime
    grid: LastDataGrid
    system: LastDataSystem
    pv: LastDataPV
    main: LastDataMain


_GRID_FIELDS: dict[str, tuple[str, type]] = {
    "gd_grid_rating_voltage": ("grid_rating_voltage", float),
    "gd_grid_rating_current": ("grid_rating_current", float),
    "gd_battery_rating_voltage": ("battery_rating_voltage", float),
    "gd_bse_input_voltage_read": ("ac_output_rating_voltage", float),
    "gd_ac_output_rating_current": ("ac_output_rating_current", float),
    "gd_bse_output_frequency_read": ("ac_output_rating_frequency", float),
    "gd_ac_output_rating_apparent_power": ("ac_output_rating_apparent_power", int),
    "gd_ac_output_rating_active_power": ("ac_output_rating_active_power", int),
}

_SYSTEM_FIELDS: dict[str, str] = {
    "sy_model": "model",
    "sy_main_cpu1_firmware_version": "main_cpu_firmware_version",
    "sy_main_cpu2_firmware_version": "secondary_cpu_firmware_version",
}

_PV_FIELDS: dict[str, tuple[str, type]] = {
    "pv_input_current": ("pv_input_current", float),
}

_MAIN_FIELDS: dict[str, tuple[str, type]] = {
    "bt_grid_voltage": ("grid_voltage", float),
    "bt_grid_frequency": ("grid_frequency", float),
    "bt_voltage_1": ("pv_input_voltage", float),
    "bt_input_power": ("pv_input_power", int),
    "bt_battery_voltage": ("battery_voltage", float),
    "bt_battery_capacity": ("battery_capacity", int),
    "bt_battery_charging_current": ("battery_charging_current", float),
    "bt_battery_discharge_current": ("battery_discharge_current", float),
    "bt_ac_output_voltage": ("ac_output_voltage", float),
    "bt_grid_AC_frequency": ("ac_output_frequency", float),
    "bt_ac_output_apparent_power": ("ac_output_apparent_power", int),
    "bt_load_active_power_sole": ("ac_output_active_power", int),
    "bt_output_load_percent": ("output_load_percent", int),
}


def _parse_typed(
    fields: list[dict[str, Any]], mapping: dict[str, tuple[str, type]]
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for entry in fields:
        spec = mapping.get(entry.get("id", ""))
        if spec is None:
            continue
        name, caster = spec
        out[name] = caster(entry["val"])
    return out


def _parse_strings(
    fields: list[dict[str, Any]], mapping: dict[str, str]
) -> dict[str, str]:
    return {
        mapping[entry["id"]]: entry["val"]
        for entry in fields
        if entry.get("id") in mapping
    }


def _parse_gts(raw: Any) -> datetime:
    """Vendor returns `gts` as either `yyyy-mm-dd HH:MM:SS` or millisecond
    epoch (string of digits). Handle both."""
    if isinstance(raw, (int, float)):
        return datetime.fromtimestamp(int(raw) / 1000.0)
    s = str(raw).strip()
    if s.isdigit():
        return datetime.fromtimestamp(int(s) / 1000.0)
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def parse_last_data(response: dict[str, Any]) -> LastData:
    """Parse a `querySPDeviceLastData` response into a `LastData` model."""
    dat = response["dat"]
    pars = dat["pars"]
    return LastData(
        timestamp=_parse_gts(dat["gts"]),
        grid=LastDataGrid(**_parse_typed(pars["gd_"], _GRID_FIELDS)),
        system=LastDataSystem(**_parse_strings(pars["sy_"], _SYSTEM_FIELDS)),
        pv=LastDataPV(**_parse_typed(pars["pv_"], _PV_FIELDS)),
        main=LastDataMain(**_parse_typed(pars["bt_"], _MAIN_FIELDS)),
    )
