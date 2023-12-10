from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
	from open_precision.core.plugin_base_classes.navigator import Navigator
	from open_precision.core.model.path import Path


class MissingPluginException(Exception):
	"""missing plugin"""

	def __init__(self, missing_plugin: str, plugin_package: str):
		self._missing_plugin = missing_plugin
		self._plugin_package = plugin_package

	def __str__(self):
		return f"no plugin of class '{self._missing_plugin}' found in package '{self._plugin_package}'"


class PluginException(Exception, ABC):
	"""subclasses can be raised by plugins"""


class SensorNotConnectedException(PluginException):
	"""raised when trying to access a sensor that is not connected"""

	def __init__(self, sensor):
		self.sensor = sensor

	def __str__(self):
		return str(self.sensor) + "is not connected"


class NotAPathException(PluginException):
	def __init__(self, path: "Path"):
		self.path = path

	def __str__(self):
		return "Path has too few waypoints, at least 2 are required"


class CourseNotSetException(PluginException):
	"""raised when there is no course set in navigator"""

	def __init__(self, navigator: Navigator):
		self.navigator = navigator

	def __str__(self):
		return f"Course of navigator {self.navigator} is None / has not been set"


class InvalidValueException(PluginException):
	"""raised when a value is invalid"""

	def __init__(self, value: Any, value_rule: str = None):
		"""
		:param value: the invalid value
		:param value_rule: a string describing the rule that the value must follow
		"""
		self.value = value
		self.value_rule = value_rule

	def __str__(self):
		if self.value_rule is None:
			return f"value {self.value} of type {type(self.value)} is invalid"
		else:
			return f"value {self.value} of type {type(self.value)} is invalid. Value rule: {self.value_rule}"
