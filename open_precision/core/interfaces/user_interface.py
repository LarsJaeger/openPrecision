from __future__ import annotations

import enum
from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from open_precision.core.interfaces.plugin import Plugin

if TYPE_CHECKING:
    from open_precision.manager import Manager


class UserInterface(Plugin, ABC):

    @abstractmethod
    def __init__(self, manager: Manager):
        # self._manager = manager
        # atexit.register(self.cleanup)
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @abstractmethod
    def get_input(self, description: str, type: type) -> any:
        pass

    class MessageType(enum.Enum):
        """
        Enum for the different message types.
        """
        INFO = 1
        WARNING = 2
        ERROR = 3
        SUCCESS = 4
        DEBUG = 5
        CRITICAL = 6
        FATAL = 7
        UNKNOWN = 8

    @abstractmethod
    def show_message(self, message: str, message_type: str):
        pass
