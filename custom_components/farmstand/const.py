"""Constants for the Lettuce Grow Farmstand Controller integration."""

DOMAIN = "farmstand"

CONF_PUMP_SWITCH = "pump_switch"
CONF_LIGHTS_SWITCH = "lights_switch"
CONF_SEASON_WEEKS = "season_weeks"
CONF_CLEANING_MINUTES = "cleaning_minutes"

DEFAULT_SEASON_WEEKS = 8
DEFAULT_CLEANING_MINUTES = 15

PLATFORMS = ["switch", "number", "button", "sensor", "datetime"]
