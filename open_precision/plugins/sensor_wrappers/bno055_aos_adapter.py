from __future__ import annotations

import atexit

import adafruit_bno055
import numpy as np
import serial
from pyquaternion import Quaternion

from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import (
    AbsoluteOrientationSensor,
)
from open_precision.system_hub import SystemHub


class Bno055AosAdapter(AbsoluteOrientationSensor):
    def __init__(self, manager: SystemHub):
        self._manager = manager
        self._manager.config.register_value(self, "bno055_serial_path", "/dev/ttyUSB0")
        self._manager.config.register_value(self, "bno055_baudrate", 115200)
        print("[Bno055AosAdapter] starting initialisation")
        uart = serial.Serial(self._manager.config.get_value(self, "bno055_serial_path"),
                             baudrate=self._manager.config.get_value(self, "bno055_baudrate"))
        self.sensor = adafruit_bno055.BNO055_UART(uart)
        self.sensor.mode = adafruit_bno055.NDOF_MODE
        # self.sensor.gyro_range = adafruit_bno055.GYRO_250_DPS
        self.sensor.accel_range = adafruit_bno055.ACCEL_2G
        atexit.register(self.cleanup)
        print("[Bno055AosAdapter] finished initialisation")

    def cleanup(self):
        pass

    @property
    def is_calibrated(self) -> bool:
        return self.sensor.calibrated

    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
        return True if calibration succeeded"""
        pass

    @property
    def scaled_acceleration(self) -> np.ndarray | None:
        return np.array(self.sensor.acceleration)

    @property
    def scaled_angular_acceleration(self) -> np.ndarray | None:
        return np.array(self.sensor.gyro)

    @property
    def scaled_magnetometer(self) -> np.ndarray | None:
        return np.array(self.sensor.magnetic)

    @property
    def orientation(self) -> Quaternion | None:
        """returns an orientation quaternion"""
        current_quat = self.sensor.quaternion
        if current_quat == (None, None, None, None):
            return None
        quat = Quaternion(current_quat)
        return quat

    @property
    def gravity(self) -> np.ndarray | None:
        """returns a gravity vector"""
        return np.array(self.sensor.gravity)
