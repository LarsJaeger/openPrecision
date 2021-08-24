import numpy as np
import qwiic_icm20948

import yaml

from openPrecision import utils

shortest_update_dt = 10 # in ms


class IMU(qwiic_icm20948.QwiicIcm20948):

    def __init__(self, config: yaml):
        super().__init__()
        if not self.connected:
            print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection")
            raise SystemError("The Qwiic ICM20948 device isn't connected to the system. Please check your connection")

        if config is None:
            self.calibrated_magnetometer_correction = np.array([0., 0., 0.])
        else:
            self.calibrated_magnetometer_correction = config['magnetometer_bias']
        self.begin()
        self._last_update = None
        self.update_values()
        self._scaled_acceleration = self.retrieve_scaled_acceleration()
        self._scaled_angular_acceleration = self.retrieve_scaled_angular_acceleration()
        self._scaled_magnetometer = self.retrieve_scaled_magnetometer()

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
            self.getAgmt()
            self._last_update = utils.millis()

    def retrieve_scaled_acceleration(self):
        if self.dataReady():
            return np.dot(np.array([self.axRaw, self.ayRaw, self.azRaw]), 1 / 16384)
        else:
            return None

    def retrieve_scaled_angular_acceleration(self):
        if self.dataReady():
            return np.dot(np.array([self.gxRaw, self.gyRaw, self.gzRaw]), 1 / 131)
        else:
            return None

    def retrieve_scaled_magnetometer(self):
        if self.dataReady():
            scaled_magnetometer = np.dot(np.array([self.mxRaw, self.myRaw, self.mzRaw]), 0.15)
            return np.add(scaled_magnetometer, self.calibrated_magnetometer_correction)
