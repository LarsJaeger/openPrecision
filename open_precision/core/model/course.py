from dataclasses import dataclass


@dataclass
class Course:
    """A course consists of paths that contain waypoints"""

    waypoints: list
