from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from open_precision.manager import Manager


class MessageType(Enum):
    """
    Enum for the different message types.
    """
    INFO = 0
    DEBUG = 1
    WARNING = 2
    SUCCESS = 3
    CRITICAL = 4
    ERROR = 5


class UserInterface(ABC):
    """
    Application Programming Interface for the Open Precision library.
    """

    @abstractmethod
    def __init__(self, manager: Manager):
        pass

    @abstractmethod
    def show_message(self, message: str, message_type: MessageType):
        pass

    @abstractmethod
    def get_input(self, description: str, type: type) -> any:
        pass
