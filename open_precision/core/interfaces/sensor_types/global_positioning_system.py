from abc import abstractmethod, ABC
from open_precision.core.interfaces.basic_sensor import BasicSensor


class GlobalPositioningSystem(BasicSensor, ABC):
    @property
    @abstractmethod
    def longitude(self) -> float:
        """returns longitude in deg"""
        pass

    @property
    @abstractmethod
    def latitude(self) -> float:
        """returns latitude in deg"""
        pass

    @property
    @abstractmethod
    def horizontal_accuracy(self):
        """returns horizontal accuracy in mm"""
        pass

    @property
    @abstractmethod
    def vertical_accuracy(self):
        """returns vertical accuracy in mm"""
        pass

    @property
    @abstractmethod
    def height_above_sea_level(self):
        """returns height above sea level in mm"""
        pass
