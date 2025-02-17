from homeassistant.components.cover import CoverEntity, CoverDeviceClass, CoverEntityFeature

from ..const import DOMAIN, BRAND

from ..nhccoco.const import PROPERTY_ACTION_VALUE_OPEN, PROPERTY_ACTION_VALUE_CLOSE, PROPERTY_ACTION_VALUE_STOP, \
    PROPERTY_STATUS_VALUE_FIXED_CLOSED
from ..nhccoco.devices.reynaers_action import CocoReynaersAction


class Nhc2ReynaersActionCoverEntity(CoverEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoReynaersAction, hub, gateway):
        """Initialize a cover."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        self._attr_is_closed = self._device.status == PROPERTY_STATUS_VALUE_FIXED_CLOSED
        self._attr_device_class = CoverDeviceClass.WINDOW
        self._attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP

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

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_open_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_OPEN)
        self.on_change()

    async def async_close_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_CLOSE)
        self.on_change()

    async def async_stop_cover(self):
        self._device.set_action(self._gateway, PROPERTY_ACTION_VALUE_STOP)
        self.on_change()
