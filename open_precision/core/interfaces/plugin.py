from __future__ import annotations

import atexit
from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager


class Plugin(ABC):
    @abstractmethod
    def __init__(self, manager: Manager):
        pass

    @abstractmethod
    def cleanup(self):
        pass
