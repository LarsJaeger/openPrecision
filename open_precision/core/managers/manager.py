from __future__ import annotations

from open_precision.core.interfaces.course_generator import CourseGenerator
from open_precision.core.interfaces.navigator import Navigator
from open_precision.core.interfaces.position_builder import PositionBuilder
from open_precision.core.managers import class_plugin_manager
from open_precision.core.managers.class_plugin_manager import PluginManager
from open_precision.core.managers.config_manager import ConfigManager
from open_precision.core.managers.vehicle_manager import VehicleManager


class Manager:
    def __init__(self):
        self._plugins = {}  # todo fix implementations
        for plugin_type in class_plugin_manager.get_classes_in_package("open_precision.core.interfaces"):
            self._plugins[plugin_type] = PluginManager(self, plugin_type, "open_precision.plugins").instance

        self._config = ConfigManager("../config.yml")
        self._sensor_manager = PluginManager(self, "open_precision.core.interfaces.sensor_types",
                                             "open_precision.plugins.sensor_wrappers")
        self._position_builder_manager = PluginManager(self, PositionBuilder,
                                                       "open_precision.plugins.position_builders")
        self._vehicles = VehicleManager(self)
        self._course_generator = PluginManager(self, CourseGenerator, "open_precision.plugins.course_generators")
        self._navigator = PluginManager(self, Navigator, "open_precision.plugins.navigators")

    @property
    def config(self) -> ConfigManager:
        return self._config

    @property
    def vehicles(self) -> VehicleManager:
        return self._vehicles

    @property
    def plugins(self) -> dict[object, any]:
        return self._plugins #todo refactor old usage
