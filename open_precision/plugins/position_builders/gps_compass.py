import yaml
from open_precision.core.interfaces.position_builder import PositionBuilder


class GpsCompassPositionBuilder(PositionBuilder):

    def __init__(self, config: yaml):
        """get available sensors"""
        pass

    def current_position(self):
        pass

    def is_ready(self):
        pass
