from __future__ import annotations

import atexit
import os
import serial
import externalTools.ublox_gps_fixed as ublox_gps
from open_precision import utils
from open_precision.core.interfaces.sensor_types.global_positioning_system import (
    GlobalPositioningSystem,
)
from open_precision.core.managers.manager import Manager

from open_precision.core.model.location import Location

shortest_update_dt = 100  # in ms


class UbloxGPSAdapter(GlobalPositioningSystem):
    def __init__(self, manager: Manager):
        self._manager = manager
        self._manager.config.register_value(self, "enable_rtk_correction", True)
        self._manager.config.register_value(
            self, "rtk_correction_start_script_path", "start_rtk.sh"
        )
        print("[UbloxGPSAdapter] starting initialisation")
        self._port = serial.Serial(
            "/dev/serial0", baudrate=115200, timeout=1
        )  # TODO add to config
        self.gps = ublox_gps.UbloxGps(self._port)
        self._correction_is_active = None
        if self._manager.config.get_value(self, "enable_rtk_correction") is True:
            self.start_rtk_correction()
            self._correction_is_active = True
        self._last_update = None
        self._message: any = None

        atexit.register(self._cleanup)
        print("[UbloxGPSAdapter] finished initialisation")

    def _cleanup(self):
        self.stop_rtk_correction()
        self._port.close()

    def update_values(self):
        if (
            self._last_update is None
            or utils.millis() - self._last_update >= shortest_update_dt
        ):
            self._message = self.gps.hp_geo_coords_ecef()
            print("message: " + str(self._message))
            self._last_update = utils.millis()

    @property
    def location(self) -> Location | None:
        self.update_values()
        if self._message is None:
            return None
        location: Location = Location(
            x=(self._message.ecefX + self._message.ecefXHp * 0.1) * 0.01,
            y=(self._message.ecefY + self._message.ecefYHp * 0.1) * 0.01,
            z=(self._message.ecefZ + self._message.ecefZHp * 0.1) * 0.01,
            error=self._message.pAcc * (10 ^ -3),
        )
        return location

    def start_rtk_correction(self):
        print("[UBloxGpsAdapter] starting RTK correction stream")
        command = "screen -dmS rtk_correction bash " + self._manager.config.get_value(
            self, "rtk_correction_start_script_path"
        )
        os.system(command)
        self._correction_is_active = True

    def stop_rtk_correction(self):
        print("[UBloxGpsAdapter] stopping RTK correction stream")
        command = "screen -r rtk_correction -X quit"
        os.system(command)
        self._correction_is_active = False
