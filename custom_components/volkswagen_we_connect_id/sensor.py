"""Sensor integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from weconnect import weconnect

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.const import (
    LENGTH_KILOMETERS,
    PERCENTAGE,
    SPEED_KILOMETERS_PER_HOUR,
    TIME_DAYS,
    TIME_MINUTES,
    UnitOfPower,
    UnitOfTemperature,
)


from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import VolkswagenIDBaseEntity, get_object_value
from .const import DOMAIN


@dataclass
class VolkswagenIdEntityDescription(SensorEntityDescription):
    """Describes Volkswagen ID sensor entity."""

    value: Callable = lambda x, y: x


SENSORS: tuple[VolkswagenIdEntityDescription, ...] = (
    VolkswagenIdEntityDescription(
        key="climatisationState",
        name="Climatisation State",
        value=lambda data: data["climatisation"][
            "climatisationStatus"
        ].climatisationState.value,
    ),
    VolkswagenIdEntityDescription(
        key="remainingClimatisationTime_min",
        name="Remaining Climatisation Time",
        native_unit_of_measurement=TIME_MINUTES,
        value=lambda data: data["climatisation"][
            "climatisationStatus"
        ].remainingClimatisationTime_min.value,
    ),
    VolkswagenIdEntityDescription(
        key="targetTemperature",
        name="Target Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value=lambda data: data["climatisation"][
            "climatisationSettings"
        ].targetTemperature_C.value,
    ),
    VolkswagenIdEntityDescription(
        key="unitInCar",
        name="Unit In car",
        value=lambda data: data["climatisation"][
            "climatisationSettings"
        ].unitInCar.value,
    ),
    VolkswagenIdEntityDescription(
        key="chargingState",
        name="Charging State",
        icon="mdi:ev-station",
        value=lambda data: data["charging"]["chargingStatus"].chargingState.value,
    ),
    VolkswagenIdEntityDescription(
        key="remainingChargingTimeToComplete_min",
        name="Remaining Charging Time",
        native_unit_of_measurement=TIME_MINUTES,
        value=lambda data: data["charging"][
            "chargingStatus"
        ].remainingChargingTimeToComplete_min.value,
    ),
    VolkswagenIdEntityDescription(
        key="chargeMode",
        name="Charging Mode",
        icon="mdi:ev-station",
        value=lambda data: data["charging"]["chargingStatus"].chargeMode.value,
    ),
    VolkswagenIdEntityDescription(
        key="chargePower_kW",
        name="Charge Power",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        value=lambda data: data["charging"]["chargingStatus"].chargePower_kW.value,
    ),
    VolkswagenIdEntityDescription(
        key="chargeRate_kmph",
        name="Charge Rate",
        native_unit_of_measurement=SPEED_KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.POWER,
        value=lambda data: data["charging"]["chargingStatus"].chargeRate_kmph.value,
    ),
    VolkswagenIdEntityDescription(
        key="chargingSettings",
        name="Charging Settings",
        value=lambda data: data["charging"]["chargingStatus"].chargingSettings.value,
    ),
    VolkswagenIdEntityDescription(
        key="chargeType",
        name="Charge Type",
        value=lambda data: data["charging"]["chargingStatus"].chargeType.value,
    ),
    VolkswagenIdEntityDescription(
        key="maxChargeCurrentAC",
        name="Max Charge Current AC",
        value=lambda data: data["charging"][
            "chargingSettings"
        ].maxChargeCurrentAC.value,
    ),
    VolkswagenIdEntityDescription(
        key="targetSOC_pct",
        name="Target State of Charge",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        value=lambda data: data["charging"]["chargingSettings"].targetSOC_pct.value,
    ),
    VolkswagenIdEntityDescription(
        key="currentSOC_pct",
        name="State of Charge",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        value=lambda data: data["charging"]["batteryStatus"].currentSOC_pct.value,
    ),
    VolkswagenIdEntityDescription(
        name="Range",
        key="cruisingRangeElectric",
        native_unit_of_measurement=LENGTH_KILOMETERS,
        value=lambda data: data["charging"][
            "batteryStatus"
        ].cruisingRangeElectric_km.value,
    ),
    VolkswagenIdEntityDescription(
        name="Health Inspection",
        key="inspectionDue",
        native_unit_of_measurement=TIME_DAYS,
        value=lambda data: data["vehicleHealthInspection"][
            "maintenanceStatus"
        ].inspectionDue_days.value,
    ),
    VolkswagenIdEntityDescription(
        name="Odometer ",
        key="odometer",
        native_unit_of_measurement=LENGTH_KILOMETERS,
        value=lambda data: data["measurements"]["odometerStatus"].odometer.value,
    ),
    VolkswagenIdEntityDescription(
        key="doorLockStatus",
        name="Door Lock Status",
        value=lambda data: data["access"]["accessStatus"].doorLockStatus.value,
    ),
    VolkswagenIdEntityDescription(
        key="bonnetLockStatus",
        name="Bonnet Lock Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["bonnet"]
        .lockState.value,
    ),
    VolkswagenIdEntityDescription(
        key="trunkLockStatus",
        name="Trunk Lock Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["trunk"]
        .lockState.value,
    ),
    VolkswagenIdEntityDescription(
        key="rearRightLockStatus",
        name="Door Rear Right Lock Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["rearRight"]
        .lockState.value,
    ),
    VolkswagenIdEntityDescription(
        key="rearLeftLockStatus",
        name="Door Rear Left Lock Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["rearLeft"]
        .lockState.value,
    ),
    VolkswagenIdEntityDescription(
        key="frontLeftLockStatus",
        name="Door Front Left Lock Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["frontLeft"]
        .lockState.value,
    ),
    VolkswagenIdEntityDescription(
        key="frontRightLockStatus",
        name="Door Right Left Lock Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["frontRight"]
        .lockState.value,
    ),
    VolkswagenIdEntityDescription(
        key="bonnetOpenStatus",
        name="Bonnet Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["bonnet"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="trunkOpenStatus",
        name="Trunk Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["trunk"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="rearRightOpenStatus",
        name="Door Rear Right Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["rearRight"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="rearLeftOpenStatus",
        name="Door Rear Left Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["rearLeft"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="frontLeftOpenStatus",
        name="Door Front Left Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["frontLeft"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="frontRightOpenStatus",
        name="Door Right Left Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .doors["frontRight"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="sunRoofStatus",
        name="Bonnet Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .windows["sunRoof"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="roofCoverStatus",
        name="Sunroof Cover Status",
        value=lambda data: data["access"]["accessStatus"]
        .windows["roofCover"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="windowRearRightOpenStatus",
        name="Window Rear Right Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .windows["rearRight"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="windowRearLeftOpenStatus",
        name="Window Rear Left Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .windows["rearLeft"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="windowFrontLeftOpenStatus",
        name="Window Front Left Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .windows["frontLeft"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="windowfrontRightOpenStatus",
        name="Window Front Right Left Open Status",
        value=lambda data: data["access"]["accessStatus"]
        .windows["frontRight"]
        .openState.value,
    ),
    VolkswagenIdEntityDescription(
        key="overallStatus",
        name="Overall Status",
        value=lambda data: data["access"]["accessStatus"].overallStatus.value,
    ),
    VolkswagenIdEntityDescription(
        key="autoUnlockPlugWhenCharged",
        name="Auto Unlock Plug When Charged",
        value=lambda data: data["charging"][
            "chargingSettings"
        ].autoUnlockPlugWhenCharged.value,
    ),
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    we_connect: weconnect.WeConnect
    we_connect = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = hass.data[DOMAIN][config_entry.entry_id + "_coordinator"]

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    entities: list[VolkswagenIDSensor] = []

    for index, vehicle in enumerate(coordinator.data):
        for sensor in SENSORS:
            entities.append(VolkswagenIDSensor(sensor, we_connect, coordinator, index))
    if entities:
        async_add_entities(entities)


class VolkswagenIDSensor(VolkswagenIDBaseEntity, SensorEntity):
    """Representation of a VolkswagenID vehicle sensor."""

    entity_description: VolkswagenIdEntityDescription

    def __init__(
        self,
        sensor: VolkswagenIdEntityDescription,
        we_connect: weconnect.WeConnect,
        coordinator: DataUpdateCoordinator,
        index: int,
    ) -> None:
        """Initialize VolkswagenID vehicle sensor."""
        super().__init__(we_connect, coordinator, index)

        self.entity_description = sensor
        self._coordinator = coordinator
        self._attr_name = f"{self.data.nickname} {sensor.name}"
        self._attr_unique_id = f"{self.data.vin}-{sensor.key}"
        if sensor.native_unit_of_measurement:
            self._attr_native_unit_of_measurement = sensor.native_unit_of_measurement
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        """Return the state."""

        state = get_object_value(self.entity_description.value(self.data.domains))
        return cast(StateType, state)
