import atexit

import numpy as np

from open_precision.core.config_manager import ConfigManager
from open_precision.core.interfaces.sensor_types.inertial_measurement_unit import InertialMeasurementUnit
import qwiic_icm20948
from open_precision import utils
from open_precision.core.exceptions import SensorNotConnectedError
from open_precision.core.plugin_manager import PluginManager

shortest_update_dt = 10  # in ms


class SparkfunIcm20948Adapter(InertialMeasurementUnit):

    def __init__(self, config_manager: ConfigManager, plugin_manager: PluginManager):
        self._plugin_manager = plugin_manager
        print('[SparkfunIcm20948Adapter] started initialisation')
        self._config_manager = config_manager.register_value(self, 'magnetometer_bias', None)
        self.imu = qwiic_icm20948.QwiicIcm20948()
        if not self.imu.connected:
            print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection")
            raise SensorNotConnectedError("Qwiic ICM20948")

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
        atexit.register(self._cleanup())
        print('[SparkfunIcm20948Adapter] finished initialisation')


    def _cleanup(self):
        pass

    @property
    def is_calibrated(self) -> bool:
        return self._config_manager.get_value(self, 'magnetometer_bias') is not None

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