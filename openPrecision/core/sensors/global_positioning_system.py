from abc import ABC, abstractmethod

import yaml


class GlobalPositioningSystem(ABC):
    @abstractmethod
    def __init__(self, config: yaml):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod(property)
    def longitude(self) -> float:
        """returns longitude in deg"""
        pass

    @abstractmethod(property)
    def latitude(self) -> float:
        """returns latitude in deg"""
        pass

    @abstractmethod(property)
    def horizontal_accuracy(self):
        """returns horizontal accuracy in mm"""
        pass

    @abstractmethod(property)
    def vertical_accuracy(self):
        """returns vertical accuracy in mm"""
        pass

    @abstractmethod(property)
    def height_above_sea_level(self):
        """returns height above sea level in mm"""
        pass
