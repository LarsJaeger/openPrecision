import math
import numpy as np
from open_precision.core.interfaces.position_builder import PositionBuilder
from open_precision.core.interfaces.sensor_types.absolute_orientation_sensor import (
    AbsoluteOrientationSensor,
)
from open_precision.core.interfaces.sensor_types.global_positioning_system import (
    GlobalPositioningSystem,
)
from open_precision.core.interfaces.sensor_types.world_magnetic_model_calculater import (
    WorldMagneticModelCalculator,
)
from open_precision.core.managers.manager import Manager
from open_precision.core.model.position import Position, Location


class GpsAosPositionBuilder(PositionBuilder):
    def __init__(self, manager: 'Manager'):
        self._manager = manager

        """get available sensors"""
        self.gps_class = GlobalPositioningSystem
        self.aos_class = AbsoluteOrientationSensor
        self.wmm_class = WorldMagneticModelCalculator

    @property
    def current_position(self) -> 'Position':
        uncorrected_location: Location = self._manager.sensors[self.gps_class].location
        orientation: np.array = self._manager.sensors[self.aos_class].orientation

        if any(x is None for x in [uncorrected_location, orientation]):
            return None
        print(f"uncorrected_locaction {uncorrected_location}")

        corrected_location = uncorrected_location + orientation.rotate(
            self._manager.vehicles.current_vehicle.gps_receiver_offset
        )

        corrected_position: Position = Position(
            location=corrected_location, orientation=orientation
        )
        return corrected_position

    @property
    def is_ready(self):
        return (
            self._manager.sensors[self.gps_class].is_calibrated()
            and self._manager.sensors[self.aos_class].is_calibrated()
        )
