from open_precision.core.interfaces.position_builder import PositionBuilder
from open_precision.core.managers.class_plugin_manager import ClassPluginManager
from open_precision.core.managers.config_manager import ConfigManager
from open_precision.core.managers.package_plugin_manager import PackagePluginManager
from open_precision.core.managers.vehicle_manager import VehicleManager


class Manager:
    def __init__(self):
        self._config = ConfigManager('../config.yml')
        self._sensors = PackagePluginManager(self,
                                             'open_precision.core.interfaces.sensor_types',
                                             'open_precision.plugins.sensor_wrappers')
        self._position_builder = ClassPluginManager(self,
                                                    PositionBuilder,
                                                    'open_precision.plugins.position_builders')
        self._vehicles = VehicleManager(self)

    @property
    def config(self):
        return self._config

    @property
    def sensors(self):
        return self._sensors

    @property
    def position_builder(self):
        return self._position_builder

    @property
    def vehicles(self):
        return self._vehicles
