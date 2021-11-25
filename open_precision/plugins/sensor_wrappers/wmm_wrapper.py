import atexit
import os
from datetime import datetime

from open_precision import utils
from open_precision.core.interfaces.sensor_types import global_positioning_system
from open_precision.core.plugin_manager import PluginManager


def wmm_input_builder(longitude: float, latitude: float, altitude_msl):
    converted_input_data_string = str(datetime.now().year) + "." + str(datetime.now().month) + " "
    converted_input_data_string += "M" + " " + "M" + str(altitude_msl) + " "
    converted_input_data_string += str(latitude) + " "
    converted_input_data_string += str(longitude)
    return converted_input_data_string


def degrees_and_minutes_to_decimal_degree(degrees, minutes):
    return degrees + (minutes * (1 / 60))


shortest_update_dt = 100  # in ms


class WmmWrapper:

    def __init__(self, config_manager, plugin_manager: PluginManager):
        self._plugin_manager = plugin_manager
        self._config_manager = config_manager.register_value(self, 'wmm_bin_path', 'example/wmm/bin/path')
        self._last_update = None
        self._current_datapoint: any = None
        self.gps = self._plugin_manager.plugin_instance_pool[global_positioning_system]
        atexit.register(self._cleanup())

    def _cleanup(self):
        pass

    def _get_data_point(self, longitude: float, latitude: float, altitude_msl):
        with open("wmmInput.txt", "w") as wmm_input:
            wmm_input.write(wmm_input_builder(longitude, latitude, altitude_msl))
        command = "cd " + self._config_manager.get_value(self, "wmm_bin_path") + " && ./wmm_file f " \
                  + str(os.getcwd()) + "/wmmInput.txt " + str(os.getcwd()) + "/wmmOutput.txt"
        print(command)
        os.system(command)
        with open("wmmOutput.txt", "r") as wwm_output:
            # read output and clean from whitespace
            result_list = wwm_output.read().splitlines()[1].split(" ")
            for number in range(result_list.count('')):
                result_list.remove('')
        result_definition_list = ['Date', 'Coord-System', 'Altitude', 'Latitude', 'Longitude', 'D_deg', 'D_min',
                                  'I_deg', 'I_min', 'H_nT', 'X_nT', 'Y_nT', 'Z_nT', 'F_nT', 'dD_min', 'dI_min', 'dH_nT',
                                  'dX_nT', 'dY_nT', 'dZ_nT', 'dF_nT']
        result_dict = dict(zip(result_definition_list, result_list))
        print(result_dict)
        return result_dict

    def update_values(self):
        if self._last_update is None or utils.millis() - self._last_update >= shortest_update_dt:
            self._current_datapoint = self._get_data_point(self.gps.longitude, self.gps.latitude,
                                                           self.gps.height_above_sea_level)
            self._last_update = utils.millis()

    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
         return True if calibration succeeded """
        pass

    @property
    def is_calibrated(self) -> bool:
        return True

    @property
    def declination(self) -> float:
        """returns the locational magnetic declination (magnetic variation) in degrees"""
        pass

    @property
    def inclination(self) -> float:
        """returns the locational magnetic inclination in degrees"""
        pass

    @property
    def total_intensity(self) -> float:
        """returns the total intensity in nT"""
        pass

    @property
    def horizontal_intensity(self) -> float:
        """returns the horizontal intensity in nT"""
        pass

    @property
    def north_component(self) -> float:
        """returns the north (X) component in nT"""
        pass

    @property
    def east_component(self) -> float:
        """returns the east (Y) component in nT"""
        pass

    @property
    def vertical_component(self) -> float:
        """returns the vertical (Z) component in nT"""
        pass

    @property
    def quaternion(self) -> float:
        """returns the quaternion describing the rotation from north to the magnetic vector"""
        pass
