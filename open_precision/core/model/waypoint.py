from dataclasses import dataclass

from open_precision.core.model.position import Location


@dataclass
class Waypoint(Location):
    id: int
    priority: int  # higher priority = more important and vice versa
    path_id: int  # id of the corresponding path
