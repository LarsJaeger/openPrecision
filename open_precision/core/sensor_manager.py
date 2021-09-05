import importlib
import inspect
from abc import ABC
from open_precision import utils


class SensorManager:
    def __init__(self):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_dir = 'open_precision.plugins.sensor_adapters'
        self.plugins = []
        self.load_plugins()

    def load_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        print(f'Looking for plugins under package {self.plugin_dir}')
        sensor_types = utils.get_classes_in_package('open_precision.core.interfaces.sensor_types')
        plugin_classes = utils.get_classes_in_package(self.plugin_dir)
        for (_, c) in plugin_classes:
            # Only add classes that are a sub class of plugin interfaces, but NOT an interface itself
            for (_, sensor_type) in sensor_types:
                if not issubclass(sensor_type, ABC):
                    break

                if issubclass(c, sensor_type) and (c is not sensor_type):
                    print(f'    Found plugin class: {c.__module__}.{c.__name__} is subclass of {sensor_type}')
                    self.plugins.append(c)
        print(f'blah {self.plugins}')
