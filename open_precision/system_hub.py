from __future__ import annotations

import asyncio
import atexit
import os.path
import traceback
from threading import Thread

from open_precision.api import API
from open_precision.managers import plugin_manager
from open_precision.managers.config_manager import ConfigManager
from open_precision.managers.data_manager import DataManager
from open_precision.managers.plugin_manager import PluginManager
from open_precision.managers.system_task_manager import SystemTaskManager
from open_precision.managers.vehicle_manager import VehicleManager


def _get_plugin_name_mapping(plugins: dict) -> dict:
    return {plugin.__name__: plugin for plugin in plugins.keys()}


class SystemHub:
    """
    reponsible for dependency injection, instance management and starting the system
    """

    def __init__(self):
        atexit.register(self._cleanup)

        # loading sub managers
        self._config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                         os.path.relpath('../config.yml'))

        self._config = ConfigManager(self)

        self._data = DataManager(self)

        self._vehicles = VehicleManager(self)

        self._system_task_manager = SystemTaskManager(self)

        # loading plugins, but loading UserInterface last
        self._plugins = {}
        for plugin_type in plugin_manager.get_classes_in_package("open_precision.core.plugin_base_classes"):
            self._plugins[plugin_type] = PluginManager(self, plugin_type, "open_precision.plugins").instance
        self._plugin_name_mapping = _get_plugin_name_mapping(self._plugins)

        # starting user interface
        self._api = API(self._system_task_manager.queue_system_task)
        api_thread = Thread(target=self._api.run)
        api_thread.start()
        asyncio.run(self._data.start_update_loop())
        api_thread.join()

    def _cleanup(self) -> None:
        # TODO replace with context managers
        try:
            for plugin in self._plugins:
                plugin.cleanup(plugin)
            self.vehicles.cleanup()
            self.config.cleanup()
        except Exception as ex:
            print("Error during cleanup:", ex)
            print(traceback.format_exc())

    @property
    def config(self) -> ConfigManager:
        return self._config

    @property
    def vehicles(self) -> VehicleManager:
        return self._vehicles

    @property
    def plugins(self) -> dict[object, any]:
        return self._plugins

    @property
    def plugin_name_mapping(self) -> dict[str, object]:
        return self._plugin_name_mapping

    @property
    def data(self) -> DataManager:
        return self._data

    @property
    def system_task_manager(self) -> SystemTaskManager:
        return self._system_task_manager

    @property
    def api(self) -> API:
        return self._api

    def reload(self):
        self._cleanup()
        self.__init__()
