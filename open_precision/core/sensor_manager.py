import importlib
import inspect

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
        for (_, c) in utils.get_classes_in_package(self.plugin_dir):
            # Only add classes that are a sub class of plugin interfaces, but NOT an interface itself
            sensor_types = utils.get_classes_in_package('open_precision.core.interfaces.sensor_types')
            for sensor_type in sensor_types:
                if issubclass(c, sensor_type) & (c is not sensor_type):
                    print(f'    Found plugin class: {c.__module__}.{c.__name__}')
                    self.plugins.append(c())