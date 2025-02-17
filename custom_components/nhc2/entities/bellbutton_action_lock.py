from homeassistant.components.lock import LockEntity

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.bellbutton_action import CocoBellbuttonAction


class Nhc2BellbuttonActionLockEntity(LockEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoBellbuttonAction, hub, gateway):
        """Initialize a lock sensor."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        self._attr_is_locked = self._device.is_doorlock_closed

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

    def lock(self, **kwargs):
        """Pass - not in use."""
        pass

    async def async_lock(self, **kwargs):
        """Pass - not in use."""
        pass

    def unlock(self, **kwargs):
        """Pass - not in use."""
        pass

    async def async_unlock(self, **kwargs):
        self._device.open_doorlock(self._gateway)
        self.on_change()
