from abc import abstractmethod


class OutputDevice:
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod(property)
    def is_operational(self):
        pass

    # TODO
