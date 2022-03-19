import atexit
import adafruit_bno055
import busio
import numpy as np
from pyquaternion import Quaternion
from open_precision.core.interfaces.sensor_types.absolute_orientation_sensor import (
    AbsoluteOrientationSensor,
)
from open_precision.core.managers.manager import Manager


class Bno055AosAdapter(AbsoluteOrientationSensor):
    def __init__(self, manager: Manager):
        self._manager = manager
        self._manager.config.register_value(self, "debug", False)
        print("[Bno055AosAdapter] starting initialisation")
        if not self._manager.config.get_value(self, "debug"):
            import board

            i2c = busio.I2C(board.SCL, board.SDA)
        else:
            print("[Bno055AosAdapter] debug mode active")
            i2c = None
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        self.sensor.mode = adafruit_bno055.NDOF_MODE
        # self.sensor.gyro_range = adafruit_bno055.GYRO_250_DPS
        self.sensor.accel_range = adafruit_bno055.ACCEL_2G
        atexit.register(self._cleanup)
        print("[Bno055AosAdapter] finished initialisation")

    def _cleanup(self):
        pass

    @property
    def is_calibrated(self) -> bool:
        return self.sensor.calibrated

    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
        return True if calibration succeeded"""
        pass

    @property
    def scaled_acceleration(self) -> np.array:
        return np.array(self.sensor.acceleration)

    @property
    def scaled_angular_acceleration(self) -> np.array:
        return np.array(self.sensor.gyro)

    @property
    def scaled_magnetometer(self) -> np.array:
        return np.array(self.sensor.magnetic)

    @property
    def orientation(self) -> Quaternion:
        """returns an orientation quaternion"""
        return Quaternion(self.sensor.quaternion) if self.sensor.quaternion is not (None, None, None, None) else None

    @property
    def gravity(self) -> np.array:
        """returns a gravity vector"""
        return np.array(self.sensor.gravity)
