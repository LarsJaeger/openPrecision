from open_precision import utils
from open_precision.core.exceptions import PluginException, MissingPluginException


def check_plugins_for_class(plugin_class, plugins) -> list:
    """returns all plugins that are a subclass of plugin_class"""

    checked_plugins = []
    for plugin in plugins:
        if issubclass(plugin, plugin_class):
            checked_plugins.append(plugin)
    return checked_plugins


class ClassPluginManager:
    def __init__(self, manager, plugin_type_class: object, plugin_package: str):
        self._manager = manager
        self._plugin_type_class = plugin_type_class
        self._plugin_package = plugin_package
        print(
            "[ClassPluginManager] loading plugin_type: "
            + str(self._plugin_type_class.__name__)
        )
        self._plugins = utils.get_classes_in_package(self._plugin_package)
        self._plugin_instance = self._initialise_plugin()
        print(
            "[ClassPluginManager] initialised plugin: "
            + str(self._plugin_instance.__class__)
        )
        print(
            "[ClassPluginManager] finished loading plugin_type: "
            + str(self.plugin_type_class.__name__)
        )

    def _initialise_plugin(self) -> object:
        # initialises first initialisable class in plugin_adapter list of available_plugins
        possible_plugins_list = check_plugins_for_class(
            self._plugin_type_class, self._plugins
        )
        if possible_plugins_list is None:
            raise MissingPluginException(self._plugin_type_class, self._plugin_package)
        for possible_plugin in possible_plugins_list:
            try:
                return possible_plugin(self._manager)
            except PluginException:
                print(
                    f"[ERROR] An error occurred while enabling {str(possible_plugin)}: {str(PluginException)}"
                )
        raise

    @property
    def instance(self):
        return self._plugin_instance

    @property
    def plugin_type_class(self):
        return self._plugin_type_class
