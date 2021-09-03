from abc import ABC, abstractmethod


class WorldMagneticModelCalculater(ABC):

    @property
    @abstractmethod
    def declination(self) -> float:
        """returns the locational magnetic declination (magnetic variation) in degrees"""
        pass

    @property
    @abstractmethod
    def inclination(self) -> float:
        """returns the locational magnetic inclination in degrees"""
        pass

    @property
    @abstractmethod
    def total_intensity(self) -> float:
        """returns the total intensity in nT"""
        pass

    @property
    @abstractmethod
    def horizontal_intensity(self) -> float:
        """returns the horizontal intensity in nT"""
        pass

    @property
    @abstractmethod
    def north_component(self) -> float:
        """returns the north (X) component in nT"""
        pass

    @property
    @abstractmethod
    def east_component(self) -> float:
        """returns the east (Y) component in nT"""
        pass

    @property
    @abstractmethod
    def vertical_component(self) -> float:
        """returns the vertical (Z) component in nT"""
        pass

    @property
    @abstractmethod
    def quaternion(self) -> float:
        """returns the north component in nT"""
        pass