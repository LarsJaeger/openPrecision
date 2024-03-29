import numpy as np
from pyquaternion import Quaternion

from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import (
	AbsoluteOrientationSensor,
)
from open_precision.system_hub import SystemHub


class AOSDummySensor(AbsoluteOrientationSensor):
	@property
	def orientation(self) -> Quaternion | None:
		return Quaternion(1, 0, 0, 0)

	@property
	def gravity(self) -> np.ndarray | None:
		return np.array([0, 0, -1], dtype=np.float64)

	def __init__(self, manager: SystemHub):
		pass

	def cleanup(self):
		pass

	@property
	def is_calibrated(self) -> bool:
		"""returns True if device is calibrated"""
		pass

	def calibrate(self) -> bool:
		"""calibrate device, (depending on your implementation also set is_calibrated accordingly) and
		return True if calibration succeeded"""
		pass
