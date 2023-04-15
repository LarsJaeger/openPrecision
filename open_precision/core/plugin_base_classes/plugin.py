from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from open_precision.managers.system_manager import SystemManager


class Plugin(ABC):
    @abstractmethod
    def __init__(self, manager: SystemManager):
        # self._manager = manager
        # atexit.register(self.cleanup)
        pass

    @abstractmethod
    def cleanup(self):
        pass
