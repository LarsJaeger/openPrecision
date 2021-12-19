import atexit
from abc import abstractmethod, ABC

from open_precision.core.managers.manager import Manager


class InputDevice(ABC):
    @abstractmethod
    def __init__(self, manager: Manager):
        self._manager = manager
        atexit.register(self._cleanup())
        pass

    @abstractmethod
    def _cleanup(self):
        pass
