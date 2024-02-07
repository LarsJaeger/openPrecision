from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from open_precision.core.model.course import Course
from open_precision.core.model.vehicle_state import VehicleState
from open_precision.core.plugin_base_classes.plugin import Plugin

if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub


class Navigator(Plugin, ABC):
	"""computes from current position and target point (or line) to output/call actions that need to be performed in
	order to the target point (or line)"""

	@abstractmethod
	def __init__(self, manager: SystemHub):
		self._manager = manager
		# atexit.register(self.cleanup)
		pass

	@abstractmethod
	def cleanup(self):
		pass

	@property
	@abstractmethod
	def current_course(self) -> Course:
		pass

	@current_course.setter
	@abstractmethod
	def current_course(self, course: Course):
		pass

	@property
	@abstractmethod
	def target_machine_state(self) -> VehicleState | None:
		pass
