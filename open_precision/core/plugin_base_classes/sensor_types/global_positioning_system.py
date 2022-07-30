from __future__ import annotations

from abc import abstractmethod, ABC
from open_precision.core.plugin_base_classes.plugin import Plugin
from open_precision.core.model.data_classes.location import Location


class GlobalPositioningSystem(Plugin, ABC):
    @property
    @abstractmethod
    def location(self) -> Location:
        """returns a Location object"""
        pass
