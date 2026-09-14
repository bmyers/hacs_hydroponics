"""Config flow for Lettuce Grow Farmstand Controller integration."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_PUMP_SWITCH,
    CONF_LIGHTS_SWITCH,
    CONF_SEASON_WEEKS,
    CONF_CLEANING_MINUTES,
    DEFAULT_SEASON_WEEKS,
    DEFAULT_CLEANING_MINUTES,
)

class FarmstandConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Farmstand Nook."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Farmstand Nook",
                data=user_input
            )

        data_schema = vol.Schema({
            vol.Required(CONF_PUMP_SWITCH): str,
            vol.Required(CONF_LIGHTS_SWITCH): str,
            vol.Optional(CONF_SEASON_WEEKS, default=DEFAULT_SEASON_WEEKS): vol.All(
                vol.Coerce(int), vol.Range(min=4, max=16)
            ),
            vol.Optional(CONF_CLEANING_MINUTES, default=DEFAULT_CLEANING_MINUTES): vol.All(
                vol.Coerce(int), vol.Range(min=1, max=60)
            ),
        })

        return self.show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return FarmstandOptionsFlowHandler()


class FarmstandOptionsFlowHandler(config_entries.OptionsFlow):
    # Remove __init__ override completely, or do not pass config_entry
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Access config_entry using built-in self.config_entry property
        options = self.config_entry.options
        data = self.config_entry.data

        options_schema = vol.Schema({
            vol.Optional(
                CONF_SEASON_WEEKS,
                default=options.get(CONF_SEASON_WEEKS, data.get(CONF_SEASON_WEEKS, DEFAULT_SEASON_WEEKS)),
            ): vol.All(vol.Coerce(int), vol.Range(min=4, max=16)),
            vol.Optional(
                CONF_CLEANING_MINUTES,
                default=options.get(CONF_CLEANING_MINUTES, data.get(CONF_CLEANING_MINUTES, DEFAULT_CLEANING_MINUTES)),
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
        })

        return self.show_form(step_id="init", data_schema=options_schema)
