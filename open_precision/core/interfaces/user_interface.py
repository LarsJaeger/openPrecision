import atexit
from abc import abstractmethod, ABC


class InputDevice(ABC):
    @abstractmethod
    def __init__(self):
        atexit.register(self._cleanup())
        pass

    @abstractmethod
    def _cleanup(self):
        pass
