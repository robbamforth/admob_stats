"""Config flow for AdMob Stats integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_CLIENT_ID, CONF_CLIENT_SECRET, CONF_REFRESH_TOKEN, CONF_PUBLISHER_ID
from .api import AdMobAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CLIENT_ID): str,
        vol.Required(CONF_CLIENT_SECRET): str,
        vol.Required(CONF_REFRESH_TOKEN): str,
        vol.Required(CONF_PUBLISHER_ID): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    api = AdMobAPI(
        client_id=data[CONF_CLIENT_ID],
        client_secret=data[CONF_CLIENT_SECRET],
        refresh_token=data[CONF_REFRESH_TOKEN],
        publisher_id=data[CONF_PUBLISHER_ID],
    )

    try:
        await hass.async_add_executor_job(api.test_connection)
    except Exception as err:
        _LOGGER.error("Failed to connect to AdMob API: %s", err)
        raise CannotConnect from err

    return {"title": f"AdMob ({data[CONF_PUBLISHER_ID]})"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AdMob Stats."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "setup_url": "https://developers.google.com/admob/api/v1/auth"
            },
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
