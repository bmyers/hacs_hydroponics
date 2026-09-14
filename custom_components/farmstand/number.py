"""Number platform for Farmstand integration."""
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, CONF_SEASON_WEEKS, CONF_CLEANING_MINUTES, DEFAULT_SEASON_WEEKS, DEFAULT_CLEANING_MINUTES

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up number entities."""
    async_add_entities([
        FarmstandCleaningTimerNumber(entry),
        FarmstandSeasonLengthNumber(entry),
    ])

class FarmstandBaseEntity:
    def __init__(self, entry: ConfigEntry):
        self._entry = entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Lettuce Grow Farmstand Nook",
            manufacturer="Lettuce Grow",
            model="Farmstand Nook",
        )

class FarmstandCleaningTimerNumber(FarmstandBaseEntity, NumberEntity):
    def __init__(self, entry: ConfigEntry):
        super().__init__(entry)
        self._attr_name = "Farmstand Cleaning Timer (Minutes)"
        self._attr_unique_id = f"{entry.entry_id}_cleaning_timer_minutes"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 60
        self._attr_native_step = 1
        self._attr_icon = "mdi:timer-outline"
        
        # Load initial value from config or default
        opts = entry.options.get(CONF_CLEANING_MINUTES, entry.data.get(CONF_CLEANING_MINUTES, DEFAULT_CLEANING_MINUTES))
        self._attr_native_value = float(opts)

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()

class FarmstandSeasonLengthNumber(FarmstandBaseEntity, NumberEntity):
    def __init__(self, entry: ConfigEntry):
        super().__init__(entry)
        self._attr_name = "Farmstand Season Length (Weeks)"
        self._attr_unique_id = f"{entry.entry_id}_season_length_weeks"
        self._attr_native_min_value = 4
        self._attr_native_max_value = 16
        self._attr_native_step = 1
        self._attr_icon = "mdi:calendar-range"
        
        # Load initial value from config or default
        opts = entry.options.get(CONF_SEASON_WEEKS, entry.data.get(CONF_SEASON_WEEKS, DEFAULT_SEASON_WEEKS))
        self._attr_native_value = float(opts)

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()
