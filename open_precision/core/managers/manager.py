from open_precision.core.managers.config_manager import ConfigManager
from open_precision.core.managers.plugin_manager import PluginManager
from open_precision.core.managers.vehicle_manager import VehicleManager


class Manager:
    def __init__(self):
        self._config = ConfigManager('../config.yml')
        self._sensors = PluginManager(self, 'open_precision.core.interfaces.sensor_types',
                                      'open_precision.plugins.sensor_wrappers')
        self._position_builders = PluginManager(self, 'open_precision.core.interfaces.position_builder',
                                                'open_precision.plugins.position_builders')
        self._vehicles = VehicleManager(self)

    @property
    def config(self):
        return self._config

    @property
    def sensors(self):
        return self._sensors

    @property
    def position_builders(self):
        return self._position_builders

    @property
    def vehicles(self):
        return self._vehicles
