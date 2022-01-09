import math

import numpy as np
from pyquaternion import Quaternion

from open_precision.core.managers.config_manager import ConfigManager
from open_precision.core.interfaces.position_builder import PositionBuilder
from open_precision.core.interfaces.sensor_types.absolute_orientation_sensor import AbsoluteOrientationSensor
from open_precision.core.interfaces.sensor_types.global_positioning_system import GlobalPositioningSystem
from open_precision.core.interfaces.sensor_types.world_magnetic_model_calculater import WorldMagneticModelCalculator
from open_precision.core.managers.manager import Manager
from open_precision.core.model.position import Position, Location
from open_precision.core.managers.package_plugin_manager import PackagePluginManager


class GpsCompassPositionBuilder(PositionBuilder):

    def __init__(self, manager: Manager):
        self._manager = manager

        """get available sensors"""
        self.gps_class = GlobalPositioningSystem
        self.aos_class = AbsoluteOrientationSensor
        self.wmm_class = WorldMagneticModelCalculator

    @property
    def current_position(self) -> Position:
        print("A")
        uncorrected_location: Location = self._manager.sensors[self.gps_class].location
        print("B")
        gravity_vector: np.ndarray = self._manager.sensors[self.aos_class].gravity
        print("C")
        mag_real_vector: np.ndarray = self._manager.sensors[self.aos_class].scaled_magnetometer
        print("D")
        mag_wmm_vector: np.ndarray = self._manager.sensors[self.wmm_class].field_vector
        print("E")
        gravity_model_vector = np.ndarray([0, 0, -1])
        print("F")
        norm_source = np.cross((-1 * gravity_vector[1]), (-1 * mag_real_vector))
        print("G")
        norm_target = np.cross(-1 * gravity_model_vector, -1 * mag_wmm_vector)
        print("H")
        source_to_target_angle = np.arccos(
            np.dot(norm_source / np.linalg.norm(norm_source), norm_target / np.linalg.norm(norm_target)))
        print("I")
        quat1: Quaternion = Quaternion(axis=np.cross(norm_source, norm_target), radians=source_to_target_angle)
        print("J")
        v1 = quat1 * (-1 * gravity_vector)
        print("K")
        v1_to_gravity_model_angle = np.arccos(np.dot(v1 / (-1 * gravity_vector), gravity_model_vector))
        print("L")
        quat2: Quaternion = Quaternion(axis=np.cross(v1, gravity_model_vector), radians=v1_to_gravity_model_angle)
        print("M")
        orientation: Quaternion = quat1 * quat2
        print("N")
        correction_vector = orientation.rotate(
            self._manager.vehicles.current_vehicle.gps_receiver_offset)  # TODO: check if it is a unit vector
        print("O")
        corrected_location: Location = Location(lon=uncorrected_location.lon -
                                                    (math.tan(correction_vector[0] /
                                                              (uncorrected_location.height - correction_vector[3]))),
                                                lat=uncorrected_location.lat -
                                                    (math.tan(correction_vector[1] /
                                                              (uncorrected_location.height - correction_vector[3]))),
                                                height=math.sqrt((uncorrected_location.height - correction_vector[3])
                                                                 ** 2 + math.sqrt(
                                                    correction_vector[0] ** 2 + correction_vector[1])) ** 2,
                                                horizontal_accuracy=0,  # TODO
                                                vertical_accuracy=0)  # TODO
        print("P")
        corrected_position: Position = Position(location=corrected_location, orientation=orientation)
        print("Q")
        return corrected_position

    @property
    def is_ready(self):
        return self._manager.sensors[self.gps_class].is_calibrated() \
               and self._manager.sensors[self.aos_class].is_calibrated() \
               and self._manager.sensors[self.wmm_class].is_calibrated()
