from __future__ import annotations

import atexit
import os
from datetime import datetime
from typing import TYPE_CHECKING

import serial
from pyubx2 import UBXReader

from open_precision.core.model.location import Location
from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import (
	GlobalPositioningSystem,
)

if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub


class UbloxGPSAdapter(GlobalPositioningSystem):
	def __init__(self, manager: SystemHub):
		self._manager = manager
		self._manager.config.register_value(self, "min_update_dt_in_ms", 100)
		self._min_update_dt = self._manager.config.get_value(
			self, "min_update_dt_in_ms"
		)
		self._manager.config.register_value(self, "enable_rtk_correction", True)
		self._manager.config.register_value(self, "rtk_str2str_in", "TODO")
		self._manager.config.register_value(self, "rtk_str2str_out", "TODO")
		self._manager.config.register_value(
			self, "ublox_F9P_serial_path", "/dev/ttyUSB1"
		)
		self._manager.config.register_value(self, "ublox_F9P_baudrate", 115200)
		print("[UbloxGPSAdapter] starting initialisation")
		self._port = serial.Serial(
			self._manager.config.get_value(self, "ublox_F9P_serial_path"),
			baudrate=self._manager.config.get_value(self, "ublox_F9P_baudrate"),
		)
		self._parser = UBXReader(self._port, protfilter=2)
		self._correction_is_active = None
		if self._manager.config.get_value(self, "enable_rtk_correction"):
			self.start_rtk_correction()
		self._last_updated = None
		self._location: Location | None = None

		atexit.register(self.cleanup)
		print("[UbloxGPSAdapter] finished initialisation")

	def cleanup(self):
		self.stop_rtk_correction()
		self._port.close()

	def update_values(self):
		_current_time = datetime.now()
		if (
			self._last_updated is None
			or (_current_time - self._last_updated).total_seconds() * 1000
			>= self._min_update_dt
		):
			fail_counter = 0
			for _, parsed_data in self._parser:
				if parsed_data.identity == "NAV-HPPOSECEF":
					self._location: Location = Location(
						x=parsed_data.ecefX * 0.01,
						y=parsed_data.ecefY * 0.01,
						z=parsed_data.ecefZ * 0.01,
						error=parsed_data.pAcc * 0.001,
					)
					break
				else:
					fail_counter += 1
					if fail_counter >= 20:
						break
			self._last_updated = _current_time

	@property
	def location(self) -> Location | None:
		"""
		returns latest location
		"""
		self.update_values()
		return self._location

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
