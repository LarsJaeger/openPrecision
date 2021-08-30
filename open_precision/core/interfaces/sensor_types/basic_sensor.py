from abc import abstractmethod

import yaml


class BasicSensor:
    @abstractmethod
    def __init__(self, config: yaml):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @property
    @abstractmethod
    def is_calibrated(self) -> bool:
        pass

    @abstractmethod
    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
         return True if calibration succeeded """
        pass

    @property
    @abstractmethod
    def is_available(self):
        """returns wether sensor is connected and can be accessed"""
        pass
