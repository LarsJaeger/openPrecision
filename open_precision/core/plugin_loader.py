import inspect
import os
import pkgutil

import open_precision.utils


class PluginLoader(object):

    def __init__(self, plugin_dir):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_dir = plugin_dir
        self.plugins = []
        self.load_plugins()

    def load_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        print(f'Looking for plugins under package {self.plugin_dir}')
        for (_, c) in open_precision.utils.get_classes_in_package(self.plugin_dir):
            # Only add classes that are a sub class of plugin interfaces, but NOT an interface itself
            sensor_types = open_precision.utils.get_classes_in_package('open_precision.core.interfaces.sensor_types')
            for sensor_type in sensor_types:
                if issubclass(c, sensor_type) & (c is not sensor_type):
                    print(f'    Found plugin class: {c.__module__}.{c.__name__}')
                    self.plugins.append(c())

    def apply_all_plugins_on_value(self, argument):
        """Apply all of the plugins on the argument supplied to this function
        """
        print()
        print(f'Applying all plugins on value {argument}:')
        for plugin in self.plugins:
            print(
                f'    Applying {plugin.description} on value {argument} yields value {plugin.perform_operation(argument)}')
