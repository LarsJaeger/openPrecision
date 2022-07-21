from __future__ import annotations

import atexit
import os.path

from open_precision.managers import plugin_manager
from open_precision.managers.data_manager import DataManager
from open_precision.managers.plugin_manager import PluginManager
from open_precision.managers.config_manager import ConfigManager
from open_precision.managers.vehicle_manager import VehicleManager


class Manager:
    def __init__(self):
        atexit.register(self._cleanup)

        # loading sub managers
        self._config = ConfigManager(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                  os.path.relpath('../config.yml')))

        self._data = DataManager(self)

        self._vehicles = VehicleManager(self)

        # loading plugins, but loading UserInterface last
        self._plugins = {}
        for plugin_type in plugin_manager.get_classes_in_package("open_precision.core.interfaces"):
            self._plugins[plugin_type] = PluginManager(self, plugin_type, "open_precision.plugins").instance

    def _cleanup(self) -> None:
        # TODO evaluate if necessary
        try:
            for plugin in self._plugins:
                plugin.cleanup(plugin)
            self.vehicles.cleanup()
            self.config.cleanup()
        except Exception as ex:
            print("Error during cleanup:", ex)

    @property
    def config(self) -> ConfigManager:
        return self._config

    @property
    def vehicles(self) -> VehicleManager:
        return self._vehicles

    @property
    def plugins(self) -> dict[object, any]:
        return self._plugins

    @property
    def data(self) -> DataManager:
        return self._data