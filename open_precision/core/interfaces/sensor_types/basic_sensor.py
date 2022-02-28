import atexit
from abc import abstractmethod, ABC

from open_precision.core.managers.manager import Manager


class BasicSensor(ABC):
    @abstractmethod
    def __init__(self, manager: Manager):
        self._manager = manager
        atexit.register(self._cleanup)
        pass

    @abstractmethod
    def _cleanup(self):
        pass

    @property
    @abstractmethod
    def is_calibrated(self) -> bool:
        pass

    @abstractmethod
    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
        return True if calibration succeeded"""
        pass
