from __future__ import annotations

from datetime import datetime
from typing import Final

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CURRENCY_EURO
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_POINT_ID,
)
from .coordinator import MegaCoordinator

SENSORS: Final = [
    ("EL", "YEAR"),
    ("EL", "MONTH"),
    ("EL", "DAY"),
    ("GAS", "YEAR"),
    ("GAS", "MONTH"),
    ("GAS", "DAY"),
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    # Coordinator op basis van de entry (niet alleen entry.data)
    coordinator = MegaCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entities: list[SensorEntity] = [
        MegaCostSensor(coordinator, entry, market, interval)
        for market, interval in SENSORS
    ]
    entities.append(MegaTokenSensor(coordinator, entry))
    entities.append(MegaBillingMonthSensor(entry))

    async_add_entities(entities)


class _BaseMegaEntity(CoordinatorEntity[MegaCoordinator], SensorEntity):
    """Basisklasse met shared eigenschappen."""

    def __init__(self, coordinator: MegaCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        # Device grouping: alles onder één apparaat "Mega Energy"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data.get(CONF_POINT_ID, "unknown_point"))},
            "manufacturer": "Mega",
            "name": "Mega Energy",
            "model": "Costs API",
        }
        # We pollen niet zelf; coordinator levert updates
        self._attr_should_poll = False


class MegaCostSensor(_BaseMegaEntity):
    """Sensor voor kosten per markt/interval."""

    def __init__(self, coordinator: MegaCoordinator, entry: ConfigEntry, market: str, interval: str) -> None:
        super().__init__(coordinator, entry)
        self._market = market
        self._interval = interval

        point_id = entry.data.get(CONF_POINT_ID, "point")
        # Unieke ID: <point>_<market>_<interval>_cost
        self._attr_unique_id = f"{point_id}_{market.lower()}_{interval.lower()}_cost"
        # Naam; voor echte i18n verhuis dit naar translations/
        self._attr_name = f"Mega {market.lower()} kost {interval.lower()}"
        self._attr_native_unit_of_measurement = CURRENCY_EURO
        # device_class 'monetary' bestaat niet; we laten device_class weg

    @property
    def native_value(self):
        return self.coordinator.costs.get(f"{self._market}_{self._interval}")


class MegaTokenSensor(_BaseMegaEntity):
    """Sensor die de tokenstatus (ok/expiring/expired) toont."""

    def __init__(self, coordinator: MegaCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        point_id = entry.data.get(CONF_POINT_ID, "point")
        self._attr_unique_id = f"{point_id}_token_status"
        self._attr_name = "Mega token status"
        self._attr_icon = "mdi:key-alert"

    @property
    def native_value(self):
        return self.coordinator.token_status


class MegaBillingMonthSensor(SensorEntity):
    """Losse helper-sensor voor huidige factuurmaand (staat los van coordinator)."""

    _attr_icon = "mdi:calendar-month"

    def __init__(self, entry: ConfigEntry) -> None:
        point_id = entry.data.get(CONF_POINT_ID, "point")
        self._attr_unique_id = f"{point_id}_billing_month"
        self._attr_name = "Mega huidige factuurmaand"
        self._attr_should_poll = False

    @property
    def native_value(self):
        return datetime.now().strftime("%Y-%m")
