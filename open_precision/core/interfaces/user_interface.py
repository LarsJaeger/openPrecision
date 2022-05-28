import atexit
from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager


class UserInterface(ABC):
    @abstractmethod
    def __init__(self, manager: 'Manager'):
        self._manager = manager
        atexit.register(self._cleanup)
        pass

    @abstractmethod
    def _cleanup(self):
        pass
