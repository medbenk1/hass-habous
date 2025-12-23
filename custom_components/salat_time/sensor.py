"""Salat Time sensor for Home Assistant."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
import urllib3

import requests
from bs4 import BeautifulSoup
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DOMAIN, DEFAULT_VILLE, DEFAULT_SCAN_INTERVAL, PRAYER_NAMES

_LOGGER = logging.getLogger(__name__)

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: AddEntitiesCallback,
    discovery_info: dict | None = None,
) -> None:
    """Set up the Salat Time sensor platform."""
    ville = config.get("ville", DEFAULT_VILLE)
    scan_interval = config.get("scan_interval", DEFAULT_SCAN_INTERVAL)

    coordinator = SalatTimeCoordinator(hass, ville, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([SalatTimeSensor(coordinator, ville)])


class SalatTimeCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Salat Time data."""

    def __init__(self, hass: HomeAssistant, ville: int, scan_interval: int):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.ville = ville
        self.url = f"https://www.habous.gov.ma/prieres/horaire-api.php?ville={ville}"
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        }

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            return await self.hass.async_add_executor_job(self._fetch_data)
        except Exception as err:
            raise UpdateFailed(f"Error fetching Salat Time data: {err}") from err

    def _fetch_data(self):
        """Fetch prayer times from API."""
        response = requests.get(self.url, headers=self.headers, verify=False, timeout=10)
        response.raise_for_status()
        html_content = response.text

        # Parse the HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the table with class "horaire"
        table = soup.find("table", {"class": "horaire"})
        if table is None:
            raise ValueError("Impossible de trouver le tableau des horaires dans le HTML")

        # Extract all time cells (td with color #055D96)
        time_cells = table.find_all("td", {"style": lambda x: x and "#055D96" in str(x)})

        if len(time_cells) < 6:
            raise ValueError(f"Nombre insuffisant d'horaires trouvés: {len(time_cells)}")

        # Extract times (they are in order: Alfajr, Chourouq, Dhuhr, Asr, Maghrib, Ishae)
        times = [cell.get_text().strip() for cell in time_cells]

        current_date = datetime.now().date()

        # Parse times and create datetime objects
        data = {}
        for i, prayer_name in enumerate(["Alfajr", "Chourouq", "Dhuhr", "Asr", "Maghrib", "Ishae"]):
            time_str = times[i]
            dt = datetime.strptime(f"{current_date} {time_str}", "%Y-%m-%d %H:%M")
            data[prayer_name.lower()] = dt

        return data


class SalatTimeSensor(SensorEntity):
    """Representation of a Salat Time sensor."""

    _attr_name = "Salat Time"
    _attr_icon = "mdi:islam"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: SalatTimeCoordinator, ville: int):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._ville = ville
        self._attr_unique_id = f"salat_time_{ville}"

    @property
    def state(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        # Return the next prayer time
        now = dt_util.now()
        prayers = [
            ("alfajr", self.coordinator.data.get("alfajr")),
            ("chourouq", self.coordinator.data.get("chourouq")),
            ("dhuhr", self.coordinator.data.get("dhuhr")),
            ("asr", self.coordinator.data.get("asr")),
            ("maghrib", self.coordinator.data.get("maghrib")),
            ("ishae", self.coordinator.data.get("ishae")),
        ]

        # Find next prayer
        for prayer_name, prayer_time in prayers:
            if prayer_time and prayer_time > now:
                return prayer_name.title()

        # If no prayer found, return the first one for tomorrow
        return "Alfajr"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}

        attrs = {}
        for prayer_name, prayer_time in self.coordinator.data.items():
            if prayer_time:
                attrs[prayer_name] = prayer_time.isoformat()
                attrs[f"{prayer_name}_time"] = prayer_time.strftime("%H:%M")

        # Add next prayer info
        now = dt_util.now()
        prayers = [
            ("alfajr", self.coordinator.data.get("alfajr")),
            ("chourouq", self.coordinator.data.get("chourouq")),
            ("dhuhr", self.coordinator.data.get("dhuhr")),
            ("asr", self.coordinator.data.get("asr")),
            ("maghrib", self.coordinator.data.get("maghrib")),
            ("ishae", self.coordinator.data.get("ishae")),
        ]

        next_prayer = None
        next_prayer_time = None
        for prayer_name, prayer_time in prayers:
            if prayer_time and prayer_time > now:
                next_prayer = prayer_name
                next_prayer_time = prayer_time
                break

        if next_prayer:
            attrs["next_prayer"] = next_prayer.title()
            attrs["next_prayer_time"] = next_prayer_time.isoformat()
            time_until = next_prayer_time - now
            attrs["time_until_next"] = str(time_until).split(".")[0]  # Remove microseconds

        return attrs

    @property
    def should_poll(self):
        """No need to poll, coordinator handles it."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update the entity."""
        await self.coordinator.async_request_refresh()

