from __future__ import annotations

import atexit
import os
from datetime import datetime

import numpy as np
from pyquaternion import Quaternion

import open_precision.utils.other
from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import (
    GlobalPositioningSystem,
)
from open_precision.core.plugin_base_classes.sensor_types.world_magnetic_model_calculater import (
    WorldMagneticModelCalculator,
)
from open_precision.manager_hub import ManagerHub


def wmm_input_builder(longitude: float, latitude: float, altitude_msl):
    converted_input_data_string = (
        str(datetime.now().year) + "." + str(datetime.now().month) + " "
    )
    converted_input_data_string += "M" + " " + "M" + str(altitude_msl) + " "
    converted_input_data_string += str(latitude) + " "
    converted_input_data_string += str(longitude)
    return converted_input_data_string


def degrees_and_minutes_to_decimal_degree(degrees, minutes):
    return degrees + (minutes * (1 / 60))


shortest_update_dt = 100000  # in ms


class WmmWrapper(WorldMagneticModelCalculator):
    def __init__(self, manager: ManagerHub):
        self._manager = manager
        self._manager.config.register_value(
            self, "wmm_bin_path", "example/wmm/bin/path"
        )
        self._last_update = None
        self._current_datapoint: any = None
        atexit.register(self.cleanup)

    def cleanup(self):
        pass

    def _get_data_point(self, longitude: float, latitude: float, altitude_msl):
        with open("wmmInput.txt", "w") as wmm_input:
            wmm_input.write(wmm_input_builder(longitude, latitude, altitude_msl))
        command = (
            "cd "
            + self._manager.config.get_value(self, "wmm_bin_path")
            + " && ./wmm_file f "
            + str(os.getcwd())
            + "/wmmInput.txt "
            + str(os.getcwd())
            + "/wmmOutput.txt"
        )
        os.system(command)
        with open("wmmOutput.txt", "r") as wwm_output:
            # read output and clean from whitespace
            result_list = wwm_output.read().splitlines()[1].split(" ")
            for number in range(result_list.count("")):
                result_list.remove("")
        result_definition_list = [
            "Date",
            "Coord-System",
            "Altitude",
            "Latitude",
            "Longitude",
            "D_deg",
            "D_min",
            "I_deg",
            "I_min",
            "H_nT",
            "X_nT",
            "Y_nT",
            "Z_nT",
            "F_nT",
            "dD_min",
            "dI_min",
            "dH_nT",
            "dX_nT",
            "dY_nT",
            "dZ_nT",
            "dF_nT",
        ]
        result_dict = dict(zip(result_definition_list, result_list))
        return result_dict

    def update_values(self):
        if (
            self._last_update is None
            or open_precision.utils.other.millis() - self._last_update >= shortest_update_dt
        ):
            self._current_datapoint = self._get_data_point(
                self._manager.plugins[GlobalPositioningSystem].longitude,
                self._manager.plugins[GlobalPositioningSystem].latitude,
                self._manager.plugins[GlobalPositioningSystem].height_above_sea_level,
            )
            self._last_update = open_precision.utils.other.millis()

    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
        return True if calibration succeeded"""
        pass

    @property
    def is_calibrated(self) -> bool:
        return True

    @property
    def declination(self) -> float:
        """returns the locational magnetic declination (magnetic variation) in degrees"""
        self.update_values()
        return float(self._current_datapoint["D_deg"]) + (
            float(self._current_datapoint["D_min"]) / 60
        )

    @property
    def inclination(self) -> float:
        """returns the locational magnetic inclination in degrees"""
        self.update_values()
        return float(self._current_datapoint["I_deg"]) + (
            float(self._current_datapoint["I_min"]) / 60
        )

    @property
    def total_intensity(self) -> float:
        """returns the total intensity in nT"""
        self.update_values()
        return self._current_datapoint["F_nT"]

    @property
    def horizontal_intensity(self) -> float:
        """returns the horizontal intensity in nT"""
        self.update_values()
        return self._current_datapoint["H_nT"]

    @property
    def field_vector(self) -> np.ndarray:
        """returns the corresponting axis components as a vector in nT, X+ = north, Y+ = East, Z+ = up"""
        self.update_values()
        return np.array(
            [
                float(self._current_datapoint["X_nT"]),
                float(self._current_datapoint["Y_nT"]),
                float(self._current_datapoint["Z_nT"]),
            ]
        )

    @property
    def quaternion(self) -> Quaternion:
        """returns the quaternion describing the rotation from north to the magnetic vector"""
        self.update_values()
        return Quaternion()

    @property
    def north_component(self) -> float:
        self.update_values()
        return self._current_datapoint["X_nT"]

    @property
    def east_component(self) -> float:
        self.update_values()
        return self._current_datapoint["Y_nT"]

    @property
    def vertical_component(self) -> float:
        self.update_values()
        return self._current_datapoint["Z_nT"]
