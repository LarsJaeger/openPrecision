import math
import numpy as np
from open_precision.core.interfaces.position_builder import PositionBuilder
from open_precision.core.interfaces.sensor_types.absolute_orientation_sensor import AbsoluteOrientationSensor
from open_precision.core.interfaces.sensor_types.global_positioning_system import GlobalPositioningSystem
from open_precision.core.interfaces.sensor_types.world_magnetic_model_calculater import WorldMagneticModelCalculator
from open_precision.core.managers.manager import Manager
from open_precision.core.model.position import Position, Location


class GpsAosPositionBuilder(PositionBuilder):

    def __init__(self, manager: Manager):
        self._manager = manager

        """get available sensors"""
        self.gps_class = GlobalPositioningSystem
        self.aos_class = AbsoluteOrientationSensor
        self.wmm_class = WorldMagneticModelCalculator

    @property
    def current_position(self) -> Position:
        uncorrected_location: Location = self._manager.sensors[self.gps_class].location
        orientation: np.array = self._manager.sensors[self.aos_class].orientation

        if any(x is None for x in [uncorrected_location, orientation]):
            return None

        print(f"uncorrected_locaction {uncorrected_location}")

        correction_vector = orientation.rotate(
            self._manager.vehicles.current_vehicle.gps_receiver_offset)  # TODO: check if it is a unit vector
        print(f"correction_vector {correction_vector}")
        corrected_location: Location = Location(lat=uncorrected_location.lat -
                                                    math.tan(
                                                        np.divide(
                                                            correction_vector[1],
                                                            uncorrected_location.height - correction_vector[2],
                                                            out=np.zeros_like(correction_vector[1]),
                                                            where=(uncorrected_location.height
                                                                   - correction_vector[2]) != 0)),
                                                lon=uncorrected_location.lon -
                                                    math.tan(
                                                        np.divide(
                                                            correction_vector[0],
                                                            uncorrected_location.height - correction_vector[2],
                                                            out=np.zeros_like(correction_vector[0]),
                                                            where=(uncorrected_location.height
                                                                   - correction_vector[2]) != 0)),
                                                height=math.sqrt(
                                                    (uncorrected_location.height - correction_vector[2]) ** 2
                                                    + math.sqrt(
                                                        correction_vector[0] ** 2 + correction_vector[1] ** 2)),
                                                horizontal_accuracy=0,  # TODO
                                                vertical_accuracy=0)  # TODO
        corrected_position: Position = Position(location=corrected_location, orientation=orientation)
        return corrected_position

    @property
    def is_ready(self):
        return self._manager.sensors[self.gps_class].is_calibrated() \
               and self._manager.sensors[self.aos_class].is_calibrated()
