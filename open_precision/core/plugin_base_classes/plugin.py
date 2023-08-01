from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class Plugin(ABC):
    @abstractmethod
    def __init__(self, manager: SystemHub):
        # self._hub = manager
        # atexit.register(self.cleanup)
        pass

    @abstractmethod
    def cleanup(self):
        pass
