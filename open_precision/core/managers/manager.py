from __future__ import annotations

from open_precision.core.interfaces.course_generator import CourseGenerator
from open_precision.core.interfaces.navigator import Navigator
from open_precision.core.interfaces.position_builder import PositionBuilder
from open_precision.core.managers.class_plugin_manager import ClassPluginManager
from open_precision.core.managers.config_manager import ConfigManager
from open_precision.core.managers.package_plugin_manager import PackagePluginManager
from open_precision.core.managers.vehicle_manager import VehicleManager


class Manager:
    def __init__(self):
        self._config = ConfigManager("../config.yml")
        self._sensor_manager = PackagePluginManager(self, "open_precision.core.interfaces.sensor_types",
                                                    "open_precision.plugins.sensor_wrappers", )
        self._position_builder_manager = ClassPluginManager(self, PositionBuilder,
                                                            "open_precision.plugins.position_builders")
        self._vehicles = VehicleManager(self)
        self._course_generator = ClassPluginManager(self, CourseGenerator, "open_precision.plugins.course_generators")
        self._navigator = ClassPluginManager(self, Navigator, "open_precision.plugins.navigators")

    @property
    def config(self) -> ConfigManager:
        return self._config

    @property
    def sensors(self) -> dict:
        return self._sensor_manager.plugin_instance_pool

    @property
    def position_builder(self) -> PositionBuilder:
        return self._position_builder_manager.instance

    @property
    def vehicles(self) -> VehicleManager:
        return self._vehicles

    @property
    def course_generator(self) -> CourseGenerator:
        return self._course_generator.instance

    @property
    def navigator(self) -> Navigator:
        return self._navigator.instance
