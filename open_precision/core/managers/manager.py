from __future__ import annotations

import atexit

from open_precision.core.managers import plugin_manager
from open_precision.core.managers.plugin_manager import PluginManager
from open_precision.core.managers.config_manager import ConfigManager
from open_precision.core.managers.vehicle_manager import VehicleManager


class Manager:
    def __init__(self):
        atexit.register(self._cleanup)
        # loading sub managers
        self._config = ConfigManager("../config.yml")
        self._vehicles = VehicleManager(self)

        # loading plugins
        self._plugins = {}
        for plugin_type in plugin_manager.get_classes_in_package("open_precision.core.interfaces"):
            self._plugins[plugin_type] = PluginManager(self, plugin_type, "open_precision.plugins").instance

    def _cleanup(self) -> None:
        # TODO evaluate if necessary
        for plugin in self._plugins:
            plugin.cleanup(plugin)

        self.vehicles.cleanup()
        self.config.cleanup()

    @property
    def config(self) -> ConfigManager:
        return self._config

    @property
    def vehicles(self) -> VehicleManager:
        return self._vehicles

    @property
    def plugins(self) -> dict[object, any]:
        return self._plugins
