import board
import adafruit_bno055
import busio
import numpy as np
import yaml
from pyquaternion import Quaternion
import open_precision.core.sensors


class Bno055AosAdapter(open_precision.core.sensors.absolute_orientation_sensor):
    def __init__(self, config: yaml):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)

    def __del__(self):
        pass

    @property
    def scaled_acceleration(self) -> np.ndarray:
        return np.array(self.sensor.acceleration)

    @property
    def scaled_angular_acceleration(self) -> np.ndarray:
        return np.array(self.sensor.gyro)

    @property
    def scaled_magnetometer(self) -> np.ndarray:
        return np.array(self.sensor.magnetic)

    @property
    def orientation(self) -> Quaternion:
        """returns an orientation quaternion"""
        return np.array(self.sensor.euler)

    @property
    def gravity(self) -> np.ndarray:
        """returns an gravity vector"""
        return np.array(self.sensor.gravity)

    @property
    def is_calibrated(self) -> bool:
        return self.sensor.calibrated

    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
         return True if calibration succeeded"""
        # TODO
        pass
