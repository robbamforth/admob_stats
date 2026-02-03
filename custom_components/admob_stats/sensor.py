"""Sensor platform for AdMob Stats."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CURRENCY_DOLLAR
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up AdMob Stats sensor entries."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = [
        AdMobEarningsSensor(coordinator, "today", "Today Earnings"),
        AdMobEarningsSensor(coordinator, "yesterday", "Yesterday Earnings"),
        AdMobEarningsSensor(coordinator, "this_month", "This Month Earnings"),
        AdMobEarningsSensor(coordinator, "last_month", "Last Month Earnings"),
        AdMobMetricSensor(coordinator, "today", "impressions", "Today Impressions"),
        AdMobMetricSensor(coordinator, "yesterday", "impressions", "Yesterday Impressions"),
        AdMobMetricSensor(coordinator, "this_month", "impressions", "This Month Impressions"),
        AdMobMetricSensor(coordinator, "last_month", "impressions", "Last Month Impressions"),
        AdMobMetricSensor(coordinator, "today", "ad_requests", "Today Ad Requests"),
        AdMobMetricSensor(coordinator, "yesterday", "ad_requests", "Yesterday Ad Requests"),
        AdMobMetricSensor(coordinator, "this_month", "ad_requests", "This Month Ad Requests"),
        AdMobMetricSensor(coordinator, "last_month", "ad_requests", "Last Month Ad Requests"),
        AdMobMetricSensor(coordinator, "today", "clicks", "Today Clicks"),
        AdMobMetricSensor(coordinator, "yesterday", "clicks", "Yesterday Clicks"),
        AdMobMetricSensor(coordinator, "this_month", "clicks", "This Month Clicks"),
        AdMobMetricSensor(coordinator, "last_month", "clicks", "Last Month Clicks"),
    ]

    async_add_entities(entities)


class AdMobEarningsSensor(CoordinatorEntity, SensorEntity):
    """Representation of an AdMob earnings sensor."""

    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = CURRENCY_DOLLAR
    _attr_icon = "mdi:currency-usd"

    def __init__(self, coordinator, period: str, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._period = period
        self._entry_id = coordinator.config_entry.entry_id  # Add this line
        self._attr_name = f"AdMob {name}"
        self._attr_unique_id = f"admob_{period}_earnings"

    @property
    def device_info(self):
        """Return device info."""
        from .const import DOMAIN
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "AdMob Stats",
            "manufacturer": "Google",
            "model": "AdMob API",
        }

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data and self._period in self.coordinator.data:
            return self.coordinator.data[self._period].get("earnings", 0.0)
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional attributes."""
        if self.coordinator.data and self._period in self.coordinator.data:
            data = self.coordinator.data[self._period]
            return {
                "impressions": data.get("impressions", 0),
                "ad_requests": data.get("ad_requests", 0),
                "clicks": data.get("clicks", 0),
            }
        return {}



class AdMobMetricSensor(CoordinatorEntity, SensorEntity):
    """Representation of an AdMob metric sensor."""

    _attr_state_class = SensorStateClass.TOTAL

    def __init__(self, coordinator, period: str, metric: str, name: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._period = period
        self._metric = metric
        self._entry_id = coordinator.config_entry.entry_id  # Add this line
        self._attr_name = f"AdMob {name}"
        self._attr_unique_id = f"admob_{period}_{metric}"

        if metric == "impressions":
            self._attr_icon = "mdi:eye"
        elif metric == "ad_requests":
            self._attr_icon = "mdi:server-network"
        elif metric == "clicks":
            self._attr_icon = "mdi:cursor-default-click"

    @property
    def device_info(self):
        """Return device info."""
        from .const import DOMAIN
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "AdMob Stats",
            "manufacturer": "Google",
            "model": "AdMob API",
        }

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        if self.coordinator.data and self._period in self.coordinator.data:
            return self.coordinator.data[self._period].get(self._metric, 0)
        return None
