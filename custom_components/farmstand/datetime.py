"""Datetime platform for Farmstand integration."""
from datetime import date
from homeassistant.components.datetime import DateTimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.util import dt as dt_util

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up datetime entity."""
    async_add_entities([
        FarmstandSeasonStartDateTime(entry),
    ])

class FarmstandSeasonStartDateTime(DateTimeEntity):
    def __init__(self, entry: ConfigEntry):
        self._entry = entry
        self._attr_name = "Farmstand Season Start Date"
        self._attr_unique_id = f"{entry.entry_id}_season_start"
        self._attr_icon = "mdi:calendar-start"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Lettuce Grow Farmstand Nook",
            manufacturer="Lettuce Grow",
            model="Farmstand Nook",
        )
        self._attr_native_value = dt_util.now()

    async def async_set_value(self, value) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()
