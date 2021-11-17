import math

import numpy as np
from pyquaternion import Quaternion

import open_precision
from open_precision.core.config_manager import ConfigManager
from open_precision.core.interfaces.position_builder import PositionBuilder
from open_precision.core.model.position import Position, Location
from open_precision.core.plugin_manager import PluginManager


class GpsCompassPositionBuilder(PositionBuilder):

    def __init__(self, sensor_manager: PluginManager, config_manager: ConfigManager):
        self._config_manager = config_manager
        """get available sensors"""
        self.gps_class = open_precision.core.interfaces.sensor_types.global_positioning_system
        self.aos_class = 'open_precision.core.interfaces.sensor_types.absolute_orientation_system'
        self.sensor_manager = sensor_manager
        pass

    @property
    def current_position(self) -> Position:
        uncorrected_location: Location = self.sensor_manager.plugin_instance_pool[self.gps_class].location
        gravity_vector: np.ndarray = self.sensor_manager.plugin_instance_pool[self.aos_class].gravity
        mag_real_vector: np.ndarray = self.sensor_manager.plugin_instance_pool[self.aos_class].scaled_magnetometer
        mag_wmm_vector: np.ndarray = np.ndarray([1, 0, 0])  # TODO
        gravity_model_vector = np.ndarray([0, 0, -1])
        norm_source = np.cross((-1 * gravity_vector[1]), (-1 * mag_real_vector))
        norm_target = np.cross(-1 * gravity_model_vector, -1 * mag_wmm_vector)
        source_to_target_angle = np.arccos(
            np.dot(norm_source / np.linalg.norm(norm_source), norm_target / np.linalg.norm(norm_target)))
        quat1: Quaternion = Quaternion(axis=np.cross(norm_source, norm_target), radians=source_to_target_angle)
        v1 = quat1 * (-1 * gravity_vector)
        v1_to_gravity_model_angle = np.arccos(np.dot(v1 / (-1 * gravity_vector), gravity_model_vector))
        quat2: Quaternion = Quaternion(axis=np.cross(v1, gravity_model_vector), radians=v1_to_gravity_model_angle)
        orientation: Quaternion = quat1 * quat2
        corrected_location: Location = Location(lon=uncorrected_location.lon - (math.sin(angle)))
        corrected_position: Position = None
        return corrected_position

    @property
    def is_ready(self):
        pass
