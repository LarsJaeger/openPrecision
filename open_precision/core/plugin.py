from __future__ import annotations

import atexit
from abc import abstractmethod, ABC

from open_precision.core.managers.manager import Manager


class Plugin(ABC):
    @abstractmethod
    def __init__(self, manager: Manager):
        pass

    @abstractmethod
    def cleanup(self):
        pass
