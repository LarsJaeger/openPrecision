from abc import ABC, abstractmethod

from open_precision.core.managers.manager import Manager


class Navigator(ABC):
    """computes from current position and target point (or line) to output/call actions that need to be performed in
    order to the target point (or line)"""

    @abstractmethod
    def __init__(self, manager: Manager):
        pass

    @property
    @abstractmethod
    def steering_angle(self):
        return None
