from open_precision import utils
from open_precision.core.exceptions import PluginException


def _group_plugins(plugin_types, plugins):
    grouped_plugins: tuple = (list(), list())
    for plugin_type in plugin_types:
        plugins_of_type = []
        for plugin in plugins:
            if issubclass(plugin, plugin_type):
                plugins_of_type.append(plugin)
        grouped_plugins[0].append(plugin_type)
        grouped_plugins[1].append(plugins_of_type)
    return grouped_plugins


def _initialise_plugins(plugin_types, plugins, config) -> dict:
    grouped_plugins = _group_plugins(plugin_types, plugins)
    print("A: " + str(grouped_plugins))
    initialised_plugins = {}
    for plugin_type in grouped_plugins[0]:
        # initialises first initialisable class in plugin_adapter list of available_plugins
        possible_plugins_list = grouped_plugins[1][grouped_plugins[0].index(plugin_type)]
        for possible_plugin in possible_plugins_list:
            try:
                initialised_plugins.update(
                    {plugin_type: possible_plugin(config)})
                break
            except PluginException:
                print(f'[ERROR] An error occurred while enabling {str(possible_plugin)}: {str(PluginException)}')
    return initialised_plugins


class PluginManager:
    def __init__(self, config, plugin_type_package: str, plugin_package: str):
        self._plugin_type_package = plugin_type_package
        self._plugin_types = utils.get_classes_in_package(self._plugin_type_package)
        self._plugin_package = plugin_package
        self._plugins = utils.get_classes_in_package(self._plugin_package)
        self._plugin_instance_pool = _initialise_plugins(self._plugin_types, self._plugins, config)

    @property
    def plugin_instance_pool(self):
        return self._plugin_instance_pool

    @property
    def plugin_types(self):
        return self._plugin_types
