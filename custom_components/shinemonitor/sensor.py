"""Sensor platform for ShineMonitor."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from shinemonitor_api.models import DeviceIdentifier, LastData

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfApparentPower,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import ShineMonitorCoordinator


@dataclass(frozen=True, kw_only=True)
class ShineMonitorSensorDescription(SensorEntityDescription):
    """Sensor description with a value extractor."""

    value_fn: Callable[[LastData], float | int | None]


SENSORS: tuple[ShineMonitorSensorDescription, ...] = (
    ShineMonitorSensorDescription(
        key="grid_voltage",
        translation_key="grid_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        value_fn=lambda d: d.main.grid_voltage,
    ),
    ShineMonitorSensorDescription(
        key="grid_frequency",
        translation_key="grid_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        value_fn=lambda d: d.main.grid_frequency,
    ),
    ShineMonitorSensorDescription(
        key="ac_output_voltage",
        translation_key="ac_output_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        value_fn=lambda d: d.main.ac_output_voltage,
    ),
    ShineMonitorSensorDescription(
        key="ac_output_frequency",
        translation_key="ac_output_frequency",
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        value_fn=lambda d: d.main.ac_output_frequency,
    ),
    ShineMonitorSensorDescription(
        key="ac_output_active_power",
        translation_key="ac_output_active_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        value_fn=lambda d: d.main.ac_output_active_power,
    ),
    ShineMonitorSensorDescription(
        key="ac_output_apparent_power",
        translation_key="ac_output_apparent_power",
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        value_fn=lambda d: d.main.ac_output_apparent_power,
    ),
    ShineMonitorSensorDescription(
        key="output_load_percent",
        translation_key="output_load_percent",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda d: d.main.output_load_percent,
    ),
    ShineMonitorSensorDescription(
        key="pv_input_voltage",
        translation_key="pv_input_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        value_fn=lambda d: d.main.pv_input_voltage,
    ),
    ShineMonitorSensorDescription(
        key="pv_input_power",
        translation_key="pv_input_power",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.WATT,
        value_fn=lambda d: d.main.pv_input_power,
    ),
    ShineMonitorSensorDescription(
        key="battery_voltage",
        translation_key="battery_voltage",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        value_fn=lambda d: d.main.battery_voltage,
    ),
    ShineMonitorSensorDescription(
        key="battery_capacity",
        translation_key="battery_capacity",
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda d: d.main.battery_capacity,
    ),
    ShineMonitorSensorDescription(
        key="battery_charging_current",
        translation_key="battery_charging_current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        value_fn=lambda d: d.main.battery_charging_current,
    ),
    ShineMonitorSensorDescription(
        key="battery_discharge_current",
        translation_key="battery_discharge_current",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        value_fn=lambda d: d.main.battery_discharge_current,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors for every inverter on the account."""
    coordinator: ShineMonitorCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ShineMonitorSensor(coordinator, device, description)
        for device in coordinator.devices
        for description in SENSORS
    )


class ShineMonitorSensor(CoordinatorEntity[ShineMonitorCoordinator], SensorEntity):
    """Single inverter reading."""

    _attr_has_entity_name = True
    entity_description: ShineMonitorSensorDescription

    def __init__(
        self,
        coordinator: ShineMonitorCoordinator,
        device: DeviceIdentifier,
        description: ShineMonitorSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._device = device
        self._attr_unique_id = f"{device.serial_number}_{description.key}"
        model = None
        snapshot = (coordinator.data or {}).get(device.serial_number)
        if snapshot is not None:
            model = snapshot.system.model
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device.serial_number)},
            name=device.device_alias or device.serial_number,
            manufacturer=MANUFACTURER,
            model=model,
            serial_number=device.serial_number,
        )

    @property
    def available(self) -> bool:
        return (
            super().available
            and self.coordinator.data is not None
            and self._device.serial_number in self.coordinator.data
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()

    @property
    def native_value(self) -> float | int | None:
        snapshot = (self.coordinator.data or {}).get(self._device.serial_number)
        if snapshot is None:
            return None
        return self.entity_description.value_fn(snapshot)
