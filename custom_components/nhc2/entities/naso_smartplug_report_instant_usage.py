from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.naso_smartplug import CocoNasoSmartplug

import logging

_LOGGER = logging.getLogger(__name__)


class Nhc2NasoSmartplugReportInstantUsageEntity(BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoNasoSmartplug, hub, gateway):
        """Initialize a binary sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_report_instant_usage'
        self._attr_should_poll = False

        self._attr_state = self._device.is_report_instant_usage
        self._attr_state_class = None
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

        # Start reporting
        self._device.enable_report_instant_usage(self._gateway)

    @property
    def name(self) -> str:
        return 'Report Instant Usage'

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': BRAND,
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def is_on(self) -> bool:
        return self._device.is_report_instant_usage

    def on_change(self):
        # Re-enable reporting when it is turned off
        if self._device.is_report_instant_usage is False:
            _LOGGER.debug(f'{self.name} re-enabled')
            self._device.enable_report_instant_usage(self._gateway)

        self.schedule_update_ha_state()
