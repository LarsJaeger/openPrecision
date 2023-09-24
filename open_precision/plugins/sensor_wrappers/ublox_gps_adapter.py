from __future__ import annotations

import atexit
import os
from typing import TYPE_CHECKING

import serial
from datetime import datetime
from ublox_gps import ublox_gps

import open_precision.utils.other
from open_precision.core.model.location import Location
from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import GlobalPositioningSystem

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class UbloxGPSAdapter(GlobalPositioningSystem):
    def __init__(self, manager: SystemHub):
        self._manager = manager
        self._manager.config.register_value(self, "min_update_dt_in_ms", 100)
        self._min_update_dt = self._manager.config.get_value(self, "min_update_dt_in_ms")
        self._manager.config.register_value(self, "enable_rtk_correction", True)
        self._manager.config.register_value(
            self, "rtk_str2str_in", "TODO"
        )
        self._manager.config.register_value(
            self, "rtk_str2str_out", "TODO"
        )
        self._manager.config.register_value(self, "ublox_F9P_serial_path", "/dev/ttyUSB1")
        self._manager.config.register_value(self, "ublox_F9P_baudrate", 115200)
        print("[UbloxGPSAdapter] starting initialisation")
        self._port = serial.Serial(
            self._manager.config.get_value(self, "ublox_F9P_serial_path"),
            baudrate=self._manager.config.get_value(self, "ublox_F9P_baudrate")
        )
        self.gps = ublox_gps.UbloxGps(hard_port=self._port)
        self._correction_is_active = None
        if self._manager.config.get_value(self, "enable_rtk_correction"):
            self.start_rtk_correction()
            self._correction_is_active = True
        self._last_updated = None
        self._message: any = None

        atexit.register(self.cleanup)
        print("[UbloxGPSAdapter] finished initialisation")

    def cleanup(self):
        self.stop_rtk_correction()
        self._port.close()

    def update_values(self):
        _current_time = datetime.now()
        if (
                self._last_updated is None
                or (_current_time - self._last_updated).total_seconds() * 1000 >= self._min_update_dt
        ):
            for i in range(10):
                self._message = self.gps.hp_geo_coords_ecef()
                if self._message is not None:
                    break
            if self._message is None:
                print("[UbloxGPSAdapter] could not get message")
            self._last_updated = _current_time

    @property
    def location(self) -> Location | None:
        self.update_values()
        if self._message is None:
            return None
        """
        message is according to 5.14.5 from https://cdn.sparkfun.com/assets/f/7/4/3/5/PM-15136.pdf
        high precision variables have already been scaled from mm to cm by library, so they can be added directly
        then both are scaled to m
        """
        location: Location = Location(
            x=(self._message.ecefX + self._message.ecefXHp) * 0.01,
            y=(self._message.ecefY + self._message.ecefYHp) * 0.01,
            z=(self._message.ecefZ + self._message.ecefZHp) * 0.01,
            error=self._message.pAcc * 0.01,
        )
        return location

    def start_rtk_correction(self):
        print("[UBloxGpsAdapter] starting RTK correction stream")
        command = f"screen -dmS rtk_correction ./app/rtklib/str2str -in {self._manager.config.get_value(self, 'rtk_str2str_in')} -out {self._manager.config.get_value(self, 'rtk_str2str_out')}"
        os.system(command)
        self._correction_is_active = True

    def stop_rtk_correction(self):
        print("[UBloxGpsAdapter] stopping RTK correction stream")
        command = "screen -r rtk_correction -X quit"
        os.system(command)
        self._correction_is_active = False
