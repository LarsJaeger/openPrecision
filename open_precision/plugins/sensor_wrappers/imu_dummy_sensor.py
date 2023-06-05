from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from open_precision.core.plugin_base_classes.sensor_types.inertial_measurement_unit import InertialMeasurementUnit

if TYPE_CHECKING:
    from open_precision.manager_hub import ManagerHub


class IMUDummySensor(InertialMeasurementUnit):
    @property
    def scaled_acceleration(self) -> np.ndarray | None:
        return np.array([0, 0, 0], dtype=np.float64)

    @property
    def scaled_angular_acceleration(self) -> np.ndarray | None:
        return np.array([0, 0, 0], dtype=np.float64)

    @property
    def scaled_magnetometer(self) -> np.ndarray | None:
        return np.array([1, 0, 0], dtype=np.float64)

    def __init__(self, manager: ManagerHub):
        pass

    def cleanup(self):
        pass