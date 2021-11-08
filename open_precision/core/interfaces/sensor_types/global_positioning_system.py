from abc import abstractmethod, ABC
from open_precision.core.interfaces.sensor_types.basic_sensor import BasicSensor
from open_precision.core.model.position import Location


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
    def horizontal_accuracy(self) -> int:
        """returns horizontal accuracy in mm"""
        pass

    @property
    @abstractmethod
    def vertical_accuracy(self) -> int:
        """returns vertical accuracy in mm"""
        pass

    @property
    @abstractmethod
    def height_above_sea_level(self) -> int:
        """returns height above sea level in mm"""
        pass

    @property
    @abstractmethod
    def location(self) -> Location:
        """returns a Location object"""
        pass