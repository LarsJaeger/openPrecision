from dataclasses import dataclass, field

from open_precision.core.model.path import Path
from open_precision.core.model.position import Location


@dataclass
class Waypoint:
    priority: int = field(init=True, default=0)  # higher priority = more important and vice versa
    location: Location = field(init=True, default=None)
    path: Path = field(init=False, default=None)
