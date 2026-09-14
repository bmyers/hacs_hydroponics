"""Button platform for Farmstand integration."""
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up button entities."""
    async_add_entities([
        FarmstandResetButton(entry, "water", "Reset Water & Nutrients Alert", "mdi:water-check"),
        FarmstandResetButton(entry, "ph", "Reset pH Alert", "mdi:check-bold"),
        FarmstandResetButton(entry, "clean", "Reset Deep Clean Alert", "mdi:check-all"),
        FarmstandResetButton(entry, "seed", "Reset Seed Propagation Alert", "mdi:sprout-outline"),
    ])

class FarmstandResetButton(ButtonEntity):
    def __init__(self, entry: ConfigEntry, key: str, name: str, icon: str):
        self._entry = entry
        self._key = key
        self._attr_name = f"Farmstand Action: {name}"
        self._attr_unique_id = f"{entry.entry_id}_reset_{key}"
        self._attr_icon = icon
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Lettuce Grow Farmstand Nook",
            manufacturer="Lettuce Grow",
            model="Farmstand Nook",
        )

    async def async_press(self) -> None:
        """Handle button press to turn off corresponding alert switch."""
        alert_entity_id = f"switch.farmstand_alert_{self._key}"
        # Turn off alert switch if on
        if self.hass.states.get(alert_entity_id):
            await self.hass.services.async_call(
                "switch",
                "turn_off",
                {"entity_id": alert_entity_id},
                blocking=True
            )
