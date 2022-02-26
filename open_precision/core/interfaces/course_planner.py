from abc import ABC

from open_precision.core.managers.manager import Manager
from open_precision.core.model.position import Position
from open_precision.core.model.waypoint import Waypoint


class CoursePlanner(ABC):
    """Generates a Path and outputs next position based on position (and last actions)"""
    def __init__(self, manager: Manager):
        pass

    def generate_course(self):
        pass

    def check_waypoint(self, waypoint: Waypoint):
        pass

    def get_waypoint(self, position: Position) -> Waypoint:
        pass
