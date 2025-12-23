"""Salat Time sensor for Home Assistant."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
import urllib3

import requests
from bs4 import BeautifulSoup
from homeassistant.components.sensor import SensorEntity, SensorStateClass
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
    _LOGGER.debug("Setting up Salat Time platform with config: %s", config)
    
    ville = config.get("ville", DEFAULT_VILLE)
    scan_interval = config.get("scan_interval", DEFAULT_SCAN_INTERVAL)
    
    _LOGGER.info("Initializing Salat Time sensor for ville=%s, scan_interval=%s", ville, scan_interval)

    try:
        coordinator = SalatTimeCoordinator(hass, ville, scan_interval)
        
        # Fetch initial data (non-blocking, will retry if it fails)
        try:
            await coordinator.async_refresh()
            _LOGGER.info("Salat Time coordinator initialized successfully")
        except Exception as refresh_err:
            _LOGGER.warning("Initial refresh failed, will retry on next update: %s", refresh_err)
        
        # Create individual sensors for each prayer
        entities = [
            PrayerTimeSensor(coordinator, ville, "alfajr", "Alfajr", "mdi:weather-sunset-up"),
            PrayerTimeSensor(coordinator, ville, "chourouq", "Chourouq", "mdi:weather-sunset"),
            PrayerTimeSensor(coordinator, ville, "dhuhr", "Dhuhr", "mdi:weather-sunny"),
            PrayerTimeSensor(coordinator, ville, "asr", "Asr", "mdi:weather-partly-cloudy"),
            PrayerTimeSensor(coordinator, ville, "maghrib", "Maghrib", "mdi:weather-sunset-down"),
            PrayerTimeSensor(coordinator, ville, "ishae", "Ishae", "mdi:weather-night"),
            NextPrayerSensor(coordinator, ville),  # Keep the next prayer sensor
        ]
        
        async_add_entities(entities)
    except Exception as err:
        _LOGGER.error("Error setting up Salat Time platform: %s", err, exc_info=True)
        raise


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

        # Get current date in local timezone
        now = dt_util.now()
        current_date = now.date()

        # Parse times and create timezone-aware datetime objects
        data = {}
        for i, prayer_name in enumerate(["Alfajr", "Chourouq", "Dhuhr", "Asr", "Maghrib", "Ishae"]):
            time_str = times[i]
            # Create naive datetime first
            dt_naive = datetime.strptime(f"{current_date} {time_str}", "%Y-%m-%d %H:%M")
            # Convert to timezone-aware using local timezone
            dt = dt_util.as_local(dt_naive)
            data[prayer_name.lower()] = dt

        return data


class PrayerTimeSensor(SensorEntity):
    """Representation of a single prayer time sensor."""

    _attr_icon = "mdi:islam"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: SalatTimeCoordinator, ville: int, prayer_key: str, prayer_name: str, icon: str):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._ville = ville
        self._prayer_key = prayer_key
        self._prayer_name = prayer_name
        self._attr_name = f"Salat {prayer_name}"
        self._attr_unique_id = f"salat_time_{ville}_{prayer_key}"
        self._attr_icon = icon

    @property
    def state(self):
        """Return the state of the sensor (time as HH:MM)."""
        if not self.coordinator.data:
            return None

        prayer_time = self.coordinator.data.get(self._prayer_key)
        if prayer_time:
            return prayer_time.strftime("%H:%M")
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}

        prayer_time = self.coordinator.data.get(self._prayer_key)
        if not prayer_time:
            return {}

        attrs = {
            "datetime": prayer_time.isoformat(),
            "timestamp": prayer_time.timestamp(),
        }

        # Add time until this prayer
        now = dt_util.now()
        if prayer_time > now:
            time_until = prayer_time - now
            attrs["time_until"] = str(time_until).split(".")[0]  # Remove microseconds
            attrs["is_passed"] = False
        else:
            attrs["is_passed"] = True

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


class NextPrayerSensor(SensorEntity):
    """Representation of the next prayer sensor."""

    _attr_name = "Salat Next Prayer"
    _attr_icon = "mdi:islam"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: SalatTimeCoordinator, ville: int):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._ville = ville
        self._attr_unique_id = f"salat_time_{ville}_next"

    @property
    def state(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        # Return the next prayer name
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

        attrs = {}
        if next_prayer and next_prayer_time:
            attrs["next_prayer"] = next_prayer.title()
            attrs["next_prayer_time"] = next_prayer_time.strftime("%H:%M")
            attrs["next_prayer_datetime"] = next_prayer_time.isoformat()
            time_until = next_prayer_time - now
            attrs["time_until"] = str(time_until).split(".")[0]  # Remove microseconds

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

