import yaml

from openPrecision import utils
from openPrecision.sensor_adapters import GPS, IMU
from openPrecision.wrappers.wmmToolWrapper import WmmToolWrapper


class AbsolutePositioningSensor:
    def __init__(self, wmm_tool_wrapper: WmmToolWrapper, gps: GPS, imu: IMU):
        self.wmm_tool_wrapper = wmm_tool_wrapper
        self.gps = gps
        self.imu = imu

    @property
    def orientation(self):
        # TODO
        return None

    @property
    def deg_from_north(self):
        local_magnetic_field = self.wmm_tool_wrapper.get_data_point(self.gps.longitude,
                                                                    self.gps.latitude,
                                                                    self.gps.height_above_sea_level)
        return local_magnetic_field - utils.declination_from_vector(self.imu.scaled_magnetometer)
