import math

import numpy as np
from pyquaternion import Quaternion
import yaml
from open_precision.core.interfaces.position_builder import PositionBuilder
from open_precision.core.model.position import Position, Location
from open_precision.core.plugin_manager import PluginManager


class GpsCompassPositionBuilder(PositionBuilder):

    def __init__(self, sensor_manager: PluginManager, config: yaml):
        """get available sensors"""
        self.gps_class = 'open_precision.core.interfaces.sensor_types.global_positioning_system'
        self.aos_class = 'open_precision.core.interfaces.sensor_types.absolute_orientation_system'
        self.sensor_manager = sensor_manager
        pass

    @property
    def current_position(self) -> Position:
        uncorrected_location: Location = self.sensor_manager.plugin_instance_pool[self.gps_class].location
        gravity_vector: np.ndarray = self.sensor_manager.plugin_instance_pool[self.aos_class].gravity
        corrected_magnetic_vector = .rotate(gravity_vector)
        orientation: Quaternion = Quaternion()<
        corrected_location: Location = Location(lon=uncorrected_location.lon - (math.sin(angle)))
        corrected_position: Position = None
        return corrected_position

    @property
    def is_ready(self):
        pass
