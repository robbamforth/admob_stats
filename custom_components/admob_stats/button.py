"""Button platform for AdMob Stats integration."""

import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up AdMob Stats button platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    async_add_entities([AdMobRefreshButton(coordinator, entry)])


class AdMobRefreshButton(ButtonEntity):
    """Button to manually refresh AdMob data."""

    def __init__(self, coordinator, entry):
        """Initialize the button."""
        self.coordinator = coordinator
        self._entry = entry
        self._attr_name = "AdMob Refresh Data"
        self._attr_unique_id = f"{entry.entry_id}_refresh_button"
        self._attr_icon = "mdi:refresh"

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "AdMob Stats",
            "manufacturer": "Google",
            "model": "AdMob API",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Manual refresh button pressed")
        await self.coordinator.async_request_refresh()
