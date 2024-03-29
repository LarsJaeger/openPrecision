from __future__ import annotations

import atexit
from datetime import datetime

import numpy as np
from pyquaternion import Quaternion

from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import (
	AbsoluteOrientationSensor,
)
from open_precision.external.bno055_serial_driver import (
	BNO055,
	AXIS_REMAP_Z,
	AXIS_REMAP_Y,
	AXIS_REMAP_X,
)
import adafruit_bno055
from adafruit_extended_bus import ExtendedI2C
from open_precision.system_hub import SystemHub


class Bno055AosAdapter(AbsoluteOrientationSensor):
	def __init__(self, manager: SystemHub):
		self._manager = manager
		self._register_config()
		print("[Bno055AosAdapter] starting initialisation")

		self._read: callable = lambda: None
		"""this function contains the function that returns the quaternion"""

		# new serial implementation
		if self._manager.config.get_value(self, "bno055_use_serial"):
			self.sensor = BNO055(
				serial_port=self._manager.config.get_value(self, "bno055_serial_path")
			)
			self.sensor.begin()
			self.sensor.set_axis_remap(x=AXIS_REMAP_X, y=AXIS_REMAP_Y, z=AXIS_REMAP_Z)
			self._read = self.sensor.read_quaternion
		else:
			# init i2c
			i2c = ExtendedI2C(2)

			self.sensor = adafruit_bno055.BNO055_I2C(i2c)
			# self.sensor.mode = adafruit_bno055.NDOF_MODE
			# self.sensor.gyro_range = adafruit_bno055.GYRO_250_DPS
			# self.sensor.accel_range = adafruit_bno055.ACCEL_2G
			# self.sensor.accel_range = adafruit_bno055.ACCEL_2G
			self._read = lambda: self.sensor.quaternion

		self._calibration_quat: Quaternion = Quaternion(1.0, 0.0, 0.0, 0.0)

		# buffer variables
		self._scaled_acceleration = None
		self._scaled_angular_acceleration = None
		self._scaled_magnetometer = None
		self._orientation: Quaternion = None
		self._gravity = None

		self._last_updated: None | datetime = None
		atexit.register(self.cleanup)
		print("[Bno055AosAdapter] finished initialisation")

	def _register_config(self):
		# config for i2c init
		self._manager.config.register_value(self, "bno055_scl_pin", 3)
		self._manager.config.register_value(self, "bno055_sda_pin", 4)
		# config for uart init:
		self._manager.config.register_value(self, "bno055_use_serial", False)
		self._manager.config.register_value(self, "bno055_serial_path", "/dev/ttyUSB0")
		self._manager.config.register_value(self, "min_update_dt_in_ms", 100)
		# general config:
		self._min_update_dt = self._manager.config.get_value(
			self, "min_update_dt_in_ms"
		)

	def update_values(self):
		_current_time = datetime.now()
		if (
			self._last_updated is None
			or (_current_time - self._last_updated).total_seconds() * 1000
			>= self._min_update_dt
		):
			# self._scaled_acceleration = np.array(self.sensor.acceleration)
			# self._scaled_angular_acceleration = np.array(self.sensor.gyro)
			# self._scaled_magnetometer = np.array(self.sensor.magnetic)
			for i in range(10):
				current_quat = self._read()
				if current_quat != (None, None, None, None):
					self._orientation = Quaternion(
						(
							current_quat[0],
							current_quat[1],
							current_quat[2],
							current_quat[3],
						)
					).normalised

					break
			else:
				self._orientation = None

			# self._gravity = np.array(self.sensor.gravity)
			self._last_updated = _current_time

	def cleanup(self):
		pass

	@property
	def is_calibrated(self) -> bool:
		"""returns True if device is calibrated"""
		# return self.sensor.calibrated
		return self.sensor.get_calibration_status()[0] != 0

	def calibrate(self) -> bool:
		"""calibrate device, (depending on your implementation also set is_calibrated accordingly) and
		return True if calibration succeeded"""
		self._calibration_quat = Quaternion(self.orientation)
		return True

	@property
	def scaled_acceleration(self) -> np.ndarray | None:
		self.update_values()
		return np.array(self._scaled_acceleration)

	@property
	def scaled_angular_acceleration(self) -> np.ndarray | None:
		self.update_values()
		return self._scaled_angular_acceleration

	@property
	def scaled_magnetometer(self) -> np.ndarray | None:
		self.update_values()
		return self._scaled_magnetometer

	@property
	def orientation(self) -> Quaternion | None:
		"""returns an orientation quaternion"""
		self.update_values()
		return self._orientation * self._calibration_quat.inverse

	@property
	def gravity(self) -> np.ndarray | None:
		"""returns a gravity vector"""
		self.update_values()
		return self._gravity
