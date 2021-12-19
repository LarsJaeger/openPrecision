import atexit
import os
import serial
import externalTools.ublox_gps_fixed as ublox_gps
from open_precision import utils
from open_precision.core.interfaces.sensor_types.global_positioning_system import GlobalPositioningSystem
from open_precision.core.managers.manager import Manager
from open_precision.core.model.position import Location

shortest_update_dt = 100  # in ms


class UbloxGPSAdapter(GlobalPositioningSystem):
    @property
    def is_calibrated(self) -> bool:
        # todo
        return True

    def calibrate(self) -> bool:
        # todo
        pass

    def __init__(self, manager: Manager):
        self._manager = manager
        self._manager.config.register_value(self, 'enable_rtk_correction', True)
        self._manager.config.register_value(self, 'rtk_correction_start_script_path', 'start_rtk.sh')
        print('[UbloxGPSAdapter] starting initialisation')
        self._port = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)
        self.gps = ublox_gps.UbloxGps(self._port)
        if self._manager.config.get_value(self, 'enable_rtk_correction') is True:
            self.start_rtk_correction()
        self._last_update = None
        self._message: any = None
        # reset correction
        self._correction_is_active = None
        # self.stop_rtk_correction()

        atexit.register(self._cleanup)
        print('[UbloxGPSAdapter] finished initialisation')

    def _cleanup(self):
        self.stop_rtk_correction()
        self._port.close()

    def update_values(self):
        if self._last_update is None or utils.millis() - self._last_update >= shortest_update_dt:
            self._message = self.gps.hp_geo_coords()
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

    @property
    def location(self) -> Location:
        location: Location = Location(lon=self.longitude,
                                      lat=self.latitude,
                                      height=self.height_above_sea_level,
                                      horizontal_accuracy=self.vertical_accuracy,
                                      vertical_accuracy=self.vertical_accuracy)
        return location

    def start_rtk_correction(self):
        command = 'screen -dmS rtk_correction bash ' + \
                  self._manager.config.get_value(self, 'rtk_correction_start_script_path')
        os.system(command)
        self._correction_is_active = True

    def stop_rtk_correction(self):
        command = 'screen -r rtk_correction -X quit'
        os.system(command)
        self._correction_is_active = False
