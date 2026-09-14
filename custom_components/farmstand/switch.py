"""Switch platform for Farmstand integration."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up switch entities."""
    async_add_entities([
        FarmstandMaintenanceSwitch(entry),
        FarmstandWaterAlertSwitch(entry),
        FarmstandPhAlertSwitch(entry),
        FarmstandCleanAlertSwitch(entry),
        FarmstandSeedAlertSwitch(entry),
    ])

class FarmstandBaseEntity:
    """Base class for Farmstand entities."""
    def __init__(self, entry: ConfigEntry):
        self._entry = entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Lettuce Grow Farmstand Nook",
            manufacturer="Lettuce Grow",
            model="Farmstand Nook",
        )

class FarmstandMaintenanceSwitch(FarmstandBaseEntity, SwitchEntity):
    """Switch to control Maintenance Mode."""
    def __init__(self, entry: ConfigEntry):
        super().__init__(entry)
        self._attr_name = "Farmstand Maintenance Mode"
        self._attr_unique_id = f"{entry.entry_id}_maintenance_mode"
        self._attr_icon = "mdi:wrench-clock"
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        self.async_write_ha_state()

class FarmstandAlertSwitch(FarmstandBaseEntity, SwitchEntity):
    """Base persistent alert switch."""
    def __init__(self, entry: ConfigEntry, key: str, name: str, icon: str):
        super().__init__(entry)
        self._attr_name = f"Farmstand Alert: {name}"
        self._attr_unique_id = f"{entry.entry_id}_alert_{key}"
        self._attr_icon = icon
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        self.async_write_ha_state()

class FarmstandWaterAlertSwitch(FarmstandAlertSwitch):
    def __init__(self, entry: ConfigEntry):
        super().__init__(entry, "water", "Water & Nutrients", "mdi:water-alert")

class FarmstandPhAlertSwitch(FarmstandAlertSwitch):
    def __init__(self, entry: ConfigEntry):
        super().__init__(entry, "ph", "Check pH", "mdi:ph")

class FarmstandCleanAlertSwitch(FarmstandAlertSwitch):
    def __init__(self, entry: ConfigEntry):
        super().__init__(entry, "clean", "Deep Clean", "mdi:shower-head")

class FarmstandSeedAlertSwitch(FarmstandAlertSwitch):
    def __init__(self, entry: ConfigEntry):
        super().__init__(entry, "seed", "Start Seed Propagation", "mdi:sprout")
