from __future__ import annotations

import math

import numpy as np
from pyquaternion import Quaternion

from open_precision.core.model.machine_state import MachineState
from open_precision.core.plugin_base_classes.machine_state_builder import MachineStateBuilder
from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import (
    AbsoluteOrientationSensor,
)
from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import (
    GlobalPositioningSystem,
)
from open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater import (
    WorldMagneticModelCalculator,
)
from open_precision.manager import Manager
from open_precision.core.model.position import Position
from open_precision.core.model.location import Location
from open_precision.utils.math import norm_vector


class GpsCompassPositionBuilder(MachineStateBuilder):
    @property
    def machine_state(self) -> MachineState | None:
        pass

    def cleanup(self):
        pass

    def __init__(self, manager: Manager):
        self._manager = manager

        """get available sensors"""

    @property
    def current_position(self) -> Position | None:
        uncorrected_location: Location = self._manager.plugins[GlobalPositioningSystem].location
        gravity_vector: np.array = self._manager.plugins[AbsoluteOrientationSensor].gravity
        mag_real_vector: np.array = self._manager.plugins[AbsoluteOrientationSensor].scaled_magnetometer
        mag_wmm_vector: np.array = self._manager.plugins[WorldMagneticModelCalculator].field_vector
        gravity_model_vector = np.array([0.0, 0.0, -1.0])

        if any(
            x is None
            for x in [
                gravity_vector,
                mag_real_vector,
                mag_wmm_vector,
                gravity_model_vector,
            ]
        ):
            return None

        print(f"uncorrected_locaction {uncorrected_location}")
        print(f"gravity_vector {gravity_vector}")
        print(f"mag_real_vector {mag_real_vector}")
        print(f"mag_wmm_vector {mag_wmm_vector}")

        print(f"uncorrected_locaction {uncorrected_location}")
        print(f"gravity_vector {norm_vector(gravity_vector)}")
        print(f"mag_real_vector {norm_vector(mag_real_vector)}")
        print(f"mag_wmm_vector {norm_vector(mag_wmm_vector)}")

        anti_gravity_vector = np.dot(-1, gravity_vector)  # for simplicity
        anti_gravity_model_vector = np.dot(-1, gravity_model_vector)  # for simplicity
        norm_source = np.cross(anti_gravity_vector, np.dot(-1, mag_real_vector))
        norm_target = np.cross(anti_gravity_model_vector, np.dot(-1, mag_wmm_vector))

        source_to_target_angle = np.arccos(
            np.clip(
                np.dot(norm_vector(norm_source), norm_vector(norm_target)), -1.0, 1.0
            )
        )

        quat1: Quaternion = Quaternion(
            axis=np.cross(norm_source, norm_target), radians=source_to_target_angle
        )
        v1 = quat1.rotate(anti_gravity_vector)
        v1_to_gravity_model_angle = np.arccos(
            np.clip(
                np.dot(
                    np.divide(
                        v1,
                        anti_gravity_vector,
                        out=np.zeros_like(v1),
                        where=anti_gravity_vector != 0,
                    ),
                    gravity_model_vector,
                ),
                -1.0,
                1.0,
            )
        )

        quat2: Quaternion = Quaternion(
            axis=np.cross(v1, gravity_model_vector), radians=v1_to_gravity_model_angle
        )
        orientation: Quaternion = quat1 * quat2
        correction_vector = orientation.rotate(
            self._manager.vehicles.current_vehicle.gps_receiver_offset
        )  # TODO: check if it is a unit vector
        print(f"correction_vector {correction_vector}")
        # TODO switch to ecef
        corrected_location: Location = Location(
            lat=uncorrected_location.lat
            - math.tan(
                np.divide(
                    correction_vector[1],
                    uncorrected_location.height - correction_vector[2],
                    out=np.zeros_like(correction_vector[1]),
                    where=(uncorrected_location.height - correction_vector[2]) != 0,
                )
            ),
            lon=uncorrected_location.lon
            - math.tan(
                np.divide(
                    correction_vector[0],
                    uncorrected_location.height - correction_vector[2],
                    out=np.zeros_like(correction_vector[0]),
                    where=(uncorrected_location.height - correction_vector[2]) != 0,
                )
            ),
            height=math.sqrt(
                (uncorrected_location.height - correction_vector[2]) ** 2
                + math.sqrt(correction_vector[0] ** 2 + correction_vector[1] ** 2)
            ),
            horizontal_accuracy=0,  # TODO
            vertical_accuracy=0,
        )  # TODO
        corrected_position: Position = Position(
            location=corrected_location, orientation=orientation
        )
        return corrected_position

    @property
    def is_ready(self):
        return (
            self._manager.plugins[GlobalPositioningSystem].is_calibrated()
            and self._manager.plugins[AbsoluteOrientationSensor].is_calibrated()
            and self._manager.plugins[WorldMagneticModelCalculator].is_calibrated()
        )
