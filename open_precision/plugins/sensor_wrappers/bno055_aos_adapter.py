from __future__ import annotations

import atexit

import adafruit_bno055
import numpy as np
import serial
from pyquaternion import Quaternion
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import (
    AbsoluteOrientationSensor,
)
from open_precision.system_hub import SystemHub


class Bno055AosAdapter(AbsoluteOrientationSensor):
    def __init__(self, manager: SystemHub):
        self._manager = manager
        self._manager.config.register_value(self, "bno055_serial_path", "/dev/ttyUSB0")
        print("[Bno055AosAdapter] starting initialisation")
        uart = serial.Serial(self._manager.config.get_value(self, "bno055_serial_path"),
                             baudrate=115200,
                             bytesize=EIGHTBITS,
                             parity=PARITY_NONE,
                             stopbits=STOPBITS_ONE)
        self.sensor = adafruit_bno055.BNO055_UART(uart)
        self.sensor.mode = adafruit_bno055.NDOF_MODE
        # self.sensor.gyro_range = adafruit_bno055.GYRO_250_DPS
        # self.sensor.accel_range = adafruit_bno055.ACCEL_2G bugged with UART

        # buffer variables
        self._scaled_acceleration = None
        self._scaled_angular_acceleration = None
        self._scaled_magnetometer = None
        self._orientation = None

        atexit.register(self.cleanup)
        print("[Bno055AosAdapter] finished initialisation")

    def update_values(self):
        _current_time = datetime.now()
        if (
                self._last_updated is None
                or (_current_time - self._last_updated).total_seconds() * 1000 >= self._min_update_dt
        ):
            self._scaled_acceleration = np.array(self.sensor.acceleration)
            self._scaled_angular_acceleration = np.array(self.sensor.gyro)
            self._scaled_magnetometer = np.array(self.sensor.magnetic)
            for i in range(10):
                current_quat = self.sensor.quaternion
                if current_quat != (None, None, None, None):
                    self._orientation = Quaternion(current_quat)
                    break
            else:
                self._orientation = None
            self._gravity = np.array(self.sensor.gravity)

            self._last_updated = _current_time

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
        return self._scaled_angular_acceleration

    @property
    def scaled_magnetometer(self) -> np.ndarray | None:
        return self._scaled_magnetometer

    @property
    def orientation(self) -> Quaternion | None:
        """returns an orientation quaternion"""
        return self._orientation

    @property
    def gravity(self) -> np.ndarray | None:
        """returns a gravity vector"""
        return self._gravity
