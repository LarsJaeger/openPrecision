from __future__ import annotations

import atexit
from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from open_precision.core.plugin import Plugin

if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager


class UserInterface(Plugin, ABC):
    @abstractmethod
    def __init__(self, manager: Manager):
        self._manager = manager
        atexit.register(self.cleanup)
        pass

    @abstractmethod
    def cleanup(self):
        pass
