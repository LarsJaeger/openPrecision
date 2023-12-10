from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from open_precision.core.model.course import Course
from open_precision.core.plugin_base_classes.plugin import Plugin

if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub


class CourseGenerator(Plugin, ABC):
	"""Generates a Path and outputs next position based on position (and last actions)"""

	@abstractmethod
	def __init__(self, manager: SystemHub):
		# self._hub = manager
		# atexit.register(self.cleanup)
		pass

	@abstractmethod
	def cleanup(self):
		pass

	@abstractmethod
	def generate_course(self) -> Course:
		pass
