import os

import serial
import yaml

import ublox_gps_fixed
import utils

shortest_update_dt = 100  # in ms


class GPS(ublox_gps_fixed.UbloxGps):
    def __init__(self, config: yaml):
        self._port = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)
        super().__init__(self._port)
        self.config = config
        self._last_update = None
        self._message = self.hp_geo_coords()
        # reset correction
        self._correction_is_active = None
        self.stop_rtk_correction()

    def __del__(self):
        self.stop_rtk_correction()
        self._port.close()

    def update_values(self):
        if self._last_update is None or utils.millis() - self._last_update >= shortest_update_dt:
            self._message = self.hp_geo_coords()
            self._last_update = utils.millis()

    @property
    def longitude(self):
        self.update_values()
        # returns longitude in deg
        return self._message.lon + self._message.lonHp

    @property
    def latitude(self):
        self.update_values()
        # returns latitude in deg
        return self._message.lat + self._message.latHp

    @property
    def horizontal_accuracy(self):
        self.update_values()
        # returns horizontal accuracy in mm
        return self._message.hAcc

    @property
    def vertical_accuracy(self):
        self.update_values()
        # returns vertical accuracy in mm
        return self._message.vAcc

    @property
    def height_above_sea_level(self):
        self.update_values()
        # returns height above sea level in mm
        return self._message.hMSL + self._message.hMSLHp

    def start_rtk_correction(self):
        command = 'screen -dmS rtk_correction bash ' + self.config['rtk_correction_start_script_path']
        os.system(command)
        self._correction_is_active = True

    def stop_rtk_correction(self):
        command = 'screen -r rtk_correction -X quit'
        os.system(command)
        self._correction_is_active = False
