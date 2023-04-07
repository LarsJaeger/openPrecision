from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from open_precision.core.model.machine_state import MachineState
from open_precision.core.model.orientation import Orientation

from open_precision.core.plugin_base_classes.machine_state_builder import MachineStateBuilder
from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import (
    AbsoluteOrientationSensor,
)
from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import (
    GlobalPositioningSystem,
)
from open_precision.core.model.position import Position
from open_precision.core.model.location import Location
from open_precision.managers.persistence_manager import PersistenceManager
from open_precision.utils.validation import validate_value

if TYPE_CHECKING:
    from open_precision.manager import Manager


class GpsAosPositionBuilder(MachineStateBuilder):
    @property
    def machine_state(self) -> MachineState | None:
        return MachineState(steering_angle=0, position=self.current_position, speed=0)

    def cleanup(self):
        pass

    def __init__(self, manager: Manager):
        self._manager = manager

        """get available sensors"""

    @property
    @PersistenceManager.persist_return
    def current_position(self) -> Position | None:
        uncorrected_location: Location = self._manager.plugins[GlobalPositioningSystem].location
        orientation: Orientation = self._manager.plugins[AbsoluteOrientationSensor].orientation
        gps_receiver_offset = self._manager.vehicles.current_vehicle.gps_receiver_offset

        for i, var in enumerate([uncorrected_location, orientation, gps_receiver_offset]):
            print(f"index {i}: {var}")
            validate_value(var, lambda x: True if x is not None else False, rule_description="value cannot be None")

        corrected_location = uncorrected_location + orientation.rotate(
            np.array(list(gps_receiver_offset), dtype=np.float64)
        )

        corrected_position: Position = Position(
            location=corrected_location, orientation=orientation
        )
        return corrected_position

    @property
    def is_ready(self):
        return (
            self._manager.plugins[GlobalPositioningSystem].is_calibrated()
            and self._manager.plugins[AbsoluteOrientationSensor].is_calibrated()
        )
