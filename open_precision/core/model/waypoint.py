from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from open_precision.core.model.path import Path
    from open_precision.core.model.location import Location


@dataclass(slots=True)
class Waypoint:
    priority: int = field(init=True, default=0)  # higher priority = more important and vice versa
    location: Location = field(init=True, default=None)
    path: Path = field(init=False, default=None)

    @property
    def id(self) -> int:
        """ Attention: Very resource intensive; gets index from search of current path's waypoint list"""
        return self.path.waypoints.index(self)