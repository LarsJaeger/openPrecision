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
        sensor_adapters = utils.get_classes_in_package(self.plugin_dir)
        for (name, c) in sensor_adapters:
            # Only add classes that are a sub class of plugin interfaces, but NOT an interface itself
            for (_, sensor_type) in sensor_types:
                if sensor_type is ABC:
                    continue

                if c is sensor_type:
                    break

                if issubclass(c, sensor_type):
                    print(f'    Found plugin class: {name} | {c.__module__}.{c.__name__} is subclass of {sensor_type}')
                    self.plugins.append(c)
        print(f'blah {self.plugins}')
