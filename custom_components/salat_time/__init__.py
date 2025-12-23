"""Salat Time integration for Home Assistant."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Salat Time component."""
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform(
            "sensor", DOMAIN, {}, config
        )
    )
    return True

