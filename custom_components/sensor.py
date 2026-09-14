"""Sensor platform for Farmstand integration."""
from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.util import dt as dt_util

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up sensor entities."""
    async_add_entities([
        FarmstandDaysActiveSensor(entry),
        FarmstandDaysRemainingSensor(entry),
    ])

class FarmstandBaseSensor(SensorEntity):
    def __init__(self, entry: ConfigEntry):
        self._entry = entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Lettuce Grow Farmstand Nook",
            manufacturer="Lettuce Grow",
            model="Farmstand Nook",
        )

class FarmstandDaysActiveSensor(FarmstandBaseSensor):
    def __init__(self, entry: ConfigEntry):
        super().__init__(entry)
        self._attr_name = "Farmstand Days Active"
        self._attr_unique_id = f"{entry.entry_id}_days_active"
        self._attr_native_unit_of_measurement = "days"
        self._attr_icon = "mdi:counter"

    @property
    def native_value(self):
        start_state = self.hass.states.get(f"datetime.farmstand_season_start_date")
        if not start_state or not start_state.state:
            return 0
        try:
            start_dt = dt_util.parse_datetime(start_state.state)
            if start_dt:
                delta = dt_util.now() - start_dt
                return max(0, delta.days)
        except Exception:
            pass
        return 0

class FarmstandDaysRemainingSensor(FarmstandBaseSensor):
    def __init__(self, entry: ConfigEntry):
        super().__init__(entry)
        self._attr_name = "Farmstand Days Remaining"
        self._attr_unique_id = f"{entry.entry_id}_days_remaining"
        self._attr_native_unit_of_measurement = "days"
        self._attr_icon = "mdi:timer-sand"

    @property
    def native_value(self):
        active_state = self.hass.states.get(f"sensor.farmstand_days_active")
        weeks_state = self.hass.states.get(f"number.farmstand_season_length_weeks")
        
        if not active_state or not weeks_state:
            return 0
        try:
            active_days = int(active_state.state)
            total_days = int(float(weeks_state.state) * 7)
            return max(0, total_days - active_days)
        except Exception:
            pass
        return 0
