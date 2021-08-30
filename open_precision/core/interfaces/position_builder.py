from abc import abstractmethod, ABC


class PositionBuilder(ABC):
    @property
    @abstractmethod
    def current_position(self):
        pass

    @property
    @abstractmethod
    def is_ready(self):
        pass
