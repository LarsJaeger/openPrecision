from __future__ import annotations

import numpy as np

from open_precision.core.model.orientation import Orientation
from open_precision.core.plugin_base_classes.machine_state_builder import MachineStateBuilder
from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import (
    AbsoluteOrientationSensor,
)
from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import (
    GlobalPositioningSystem,
)
from open_precision.manager import Manager
from open_precision.core.model.position import Position
from open_precision.core.model.location import Location
from open_precision.managers.persistence_manager import PersistenceManager


class GpsAosMachineStateBuilder(MachineStateBuilder):
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

        if any(x is None for x in [uncorrected_location, orientation]):
            return None
        corrected_location = uncorrected_location + orientation.rotate(
            np.array(list(self._manager.vehicles.current_vehicle.gps_receiver_offset), dtype=np.float64)
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
