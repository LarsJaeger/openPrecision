from abc import ABC

import yaml

import open_precision.core.position_builder


class GpsCompassPositionBuilder(open_precision.core.position_builder.PositionBuilder, ABC):

    def __init__(self, config: yaml):
        """get available sensors"""
        pass

    def current_position(self):
        pass

    def is_ready(self):
        pass
