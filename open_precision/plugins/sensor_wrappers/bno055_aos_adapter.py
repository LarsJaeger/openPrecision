from __future__ import annotations

import atexit
from datetime import datetime

import adafruit_bno055
import numpy as np
import serial
from pyquaternion import Quaternion
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import (
    AbsoluteOrientationSensor,
)
from open_precision.external.bno055_serial_driver import BNO055
from open_precision.system_hub import SystemHub


class Bno055AosAdapter(AbsoluteOrientationSensor):
    def __init__(self, manager: SystemHub):
        self._manager = manager
        self._manager.config.register_value(self, "bno055_serial_path", "/dev/ttyUSB0")
        self._manager.config.register_value(self, "min_update_dt_in_ms", 100)
        self._min_update_dt = self._manager.config.get_value(self, "min_update_dt_in_ms")
        print("[Bno055AosAdapter] starting initialisation")


        # new serial implementation
        self.sensor = BNO055(serial_port=self._manager.config.get_value(self, "bno055_serial_path"))
        self.sensor.begin()
        self.sensor.setExternalCrystalUse(True)

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

    def update_values(self):
        _current_time = datetime.now()
        if (
                self._last_updated is None
                or (_current_time - self._last_updated).total_seconds() * 1000 >= self._min_update_dt
        ):
            # self._scaled_acceleration = np.array(self.sensor.acceleration)
            # self._scaled_angular_acceleration = np.array(self.sensor.gyro)
            # self._scaled_magnetometer = np.array(self.sensor.magnetic)
            for i in range(10):
                current_quat = self.sensor.read_quaternion()
                if current_quat != (None, None, None, None):
                    self._orientation = Quaternion(current_quat).normalised

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
        self._calibration_quat = Quaternion(self.sensor.read_quaternion())
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
