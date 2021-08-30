from abc import abstractmethod, ABC


class InputDevice(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @property
    @abstractmethod
    def is_operational(self):
        pass

    # TODO
