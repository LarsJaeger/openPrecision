from abc import ABC

from open_precision.core.model.path import Path


class MissingPluginException(Exception):
    """missing plugin"""

    def __init__(self, missing_plugin, plugin_package):
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

    def __init__(self, path: Path):
        self.path = path

    def __str__(self):
        return f'Path has too few waypoints, at least 2 are required'
