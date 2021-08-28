import numpy as np
import open_precision.core.sensors
import qwiic_icm20948
import yaml
from open_precision import utils

shortest_update_dt = 10 # in ms


class IMU(open_precision.core.sensors.InertialMeasurementUnit):

    def __init__(self, config: yaml):
        self.config = config
        self.imu = qwiic_icm20948.QwiicIcm20948()
        if not self.imu.connected:
            print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection")
            raise SystemError("The Qwiic ICM20948 device isn't connected to the system. Please check your connection")

        if self.config is None:
            self.calibrated_magnetometer_correction = np.array([0., 0., 0.])
        else:
            self.calibrated_magnetometer_correction = self.config['magnetometer_bias']
        self.imu.begin()
        self._last_update = None
        self.update_values()
        self._scaled_acceleration = self.retrieve_scaled_acceleration()
        self._scaled_angular_acceleration = self.retrieve_scaled_angular_acceleration()
        self._scaled_magnetometer = self.retrieve_scaled_magnetometer()

    @property
    def is_calibrated(self) -> bool:
        return self.config['magnetometer_bias'] is not None

    def calibrate(self) -> bool:
        print("Please enter calibration data in config.yml and retry!")
        return False

    @property
    def scaled_acceleration(self):
        self.update_values()
        self._scaled_acceleration = self.retrieve_scaled_acceleration()
        return self._scaled_acceleration

    @property
    def scaled_angular_acceleration(self):
        self.update_values()
        self._scaled_angular_acceleration = self.retrieve_scaled_angular_acceleration()
        return self._scaled_angular_acceleration

    @property
    def scaled_magnetometer(self):
        self.update_values()
        self._scaled_magnetometer = self.retrieve_scaled_magnetometer()
        return self._scaled_magnetometer

    def update_values(self):
        if self._last_update is None or utils.millis() - self._last_update >= shortest_update_dt:
            self.imu.getAgmt()
            self._last_update = utils.millis()

    def retrieve_scaled_acceleration(self):
        if self.imu.dataReady():
            return np.dot(np.array([self.imu.axRaw, self.imu.ayRaw, self.imu.azRaw]), 1 / 16384)
        else:
            return None

    def retrieve_scaled_angular_acceleration(self):
        if self.imu.dataReady():
            return np.dot(np.array([self.imu.gxRaw, self.imu.gyRaw, self.imu.gzRaw]), 1 / 131)
        else:
            return None

    def retrieve_scaled_magnetometer(self):
        if self.imu.dataReady():
            scaled_magnetometer = np.dot(np.array([self.imu.mxRaw, self.imu.myRaw, self.imu.mzRaw]), 0.15)
            return np.add(scaled_magnetometer, self.calibrated_magnetometer_correction)
