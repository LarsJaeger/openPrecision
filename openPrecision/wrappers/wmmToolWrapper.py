import os
from datetime import datetime


def wmm_input_builder(longitude: float, latitude: float, altitude_msl):
    converted_input_data_string = str(datetime.now().year) + "." + str(datetime.now().month) + " "
    converted_input_data_string += "M" + " " + "M" + str(altitude_msl) + " "
    converted_input_data_string += str(latitude) + " "
    converted_input_data_string += str(longitude)
    return converted_input_data_string


def degrees_and_minutes_to_decimal_degree(degrees, minutes):
    return degrees + (minutes * (1 / 60))


class WmmToolWrapper:

    def __init__(self, config):
        self.config = config

    def get_data_point(self, longitude: float, latitude: float, altitude_msl):
        with open("wmmInput.txt", "w") as wmm_input:
            wmm_input.write(wmm_input_builder(longitude, latitude, altitude_msl))
        command = "cd " + self.config["wmm_bin_path"] + " && ./wmm_file f " \
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
