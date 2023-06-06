from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from open_precision.core.model import persist_return
from open_precision.core.model.position import Position
from open_precision.core.model.vehicle_state import VehicleState
from open_precision.core.plugin_base_classes.plugin import Plugin

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class MachineStateBuilder(Plugin, ABC):
    @abstractmethod
    def __init__(self, manager: SystemHub):
        # self._manager = manager
        # atexit.register(self.cleanup)
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @property
    @abstractmethod
    @persist_return
    def machine_state(self) -> VehicleState | None:
        return self.current_position

    @property
    @abstractmethod
    @persist_return
    def current_position(self) -> Position | None:
        """returns current position (location describes the location of the center of the rear axle)"""
        pass

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        pass
