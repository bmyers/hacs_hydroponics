"""Config flow for Lettuce Grow Farmstand Controller integration."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

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
        """Handle initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title="Farmstand Nook",
                data=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_PUMP_SWITCH): EntitySelector(
                    EntitySelectorConfig(domain="switch")
                ),
                vol.Required(CONF_LIGHTS_SWITCH): EntitySelector(
                    EntitySelectorConfig(domain="switch")
                ),
                vol.Optional(
                    CONF_SEASON_WEEKS, default=DEFAULT_SEASON_WEEKS
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=4, max=16, step=1, mode=NumberSelectorMode.BOX
                    )
                ),
                vol.Optional(
                    CONF_CLEANING_MINUTES, default=DEFAULT_CLEANING_MINUTES
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=1, max=60, step=1, mode=NumberSelectorMode.BOX
                    )
                ),
            }
        )

        # Fixed: Changed show_form to async_show_form
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get options flow."""
        return FarmstandOptionsFlowHandler()


class FarmstandOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options re-configuration."""

    async def async_step_init(self, user_input=None):
        """Manage options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        data = self.config_entry.data

        current_weeks = options.get(
            CONF_SEASON_WEEKS, data.get(CONF_SEASON_WEEKS, DEFAULT_SEASON_WEEKS)
        )
        current_minutes = options.get(
            CONF_CLEANING_MINUTES,
            data.get(CONF_CLEANING_MINUTES, DEFAULT_CLEANING_MINUTES),
        )

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SEASON_WEEKS, default=current_weeks
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=4, max=16, step=1, mode=NumberSelectorMode.BOX
                    )
                ),
                vol.Optional(
                    CONF_CLEANING_MINUTES, default=current_minutes
                ): NumberSelector(
                    NumberSelectorConfig(
                        min=1, max=60, step=1, mode=NumberSelectorMode.BOX
                    )
                ),
            }
        )

        # Fixed: Changed show_form to async_show_form
        return self.async_show_form(step_id="init", data_schema=options_schema)
