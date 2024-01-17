"""
This file contains the SystemHub class, which is the central backbone of every instance of the application.
"""
from __future__ import annotations

import asyncio
import os.path
import time

from open_precision.api import API
from open_precision.core.model import map_model
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
	reponsible for dependency injection, instance management, starting, reloading and stopping the system
	"""

	def __init__(self):
		self._signal_reload = True  # The system will reload if this is True
		while self._signal_reload:
			# loading sub managers
			self._config_path = os.path.join(
				os.path.abspath(os.path.dirname(__file__)),
				os.path.relpath("../config/config.yml"),
			)

			self._config = ConfigManager(self)

			# map model
			print("[INFO]: sleeping for 5 sec")
			time.sleep(5)
			print("[INFO]: starting model mapping")
			self._config.register_value(
				self, "neo4j_address", "bolt://neo4j:password@neo4j:7687"
			)
			map_model(database_url=self._config.get_value(self, "neo4j_address"))
			print("[INFO]: finished model mapping")

			self._data = DataManager(self)

			self._vehicles = VehicleManager(self)

			self._system_task_manager = SystemTaskManager(self)

			# loading plugins, but loading UserInterface last
			self._plugins = {}
			for plugin_type in plugin_manager.get_classes_in_package(
				"open_precision.core.plugin_base_classes"
			):
				self._plugins[plugin_type] = PluginManager(
					self, plugin_type, "open_precision.plugins"
				).instance
			self._plugin_name_mapping = _get_plugin_name_mapping(self._plugins)

			# initializing and starting api and user interface delivery
			self._api = API(self)
			print("[INFO]: starting api thread")
			with self._api:
				# starting update loop
				self._signal_stop = False  # the update loop will stop if this is True
				print("[INFO]: starting update loop")
				asyncio.run(self.start_update_loop())
				print("[INFO]: stopped update loop")
			print("[INFO]: stopped api thread")

	async def start_update_loop(self):
		while not self._signal_stop:
			artificial_slow_down = asyncio.sleep(0.05)

			# handle actions and deliver responses
			try:
				await self._system_task_manager.handle_tasks(amount=10)
			except Exception as e:
				print(f"[ERROR]: Error while handling system tasks: {e}")
				await self._data.emit_error(e)

			# doing data updates (of data subscriptions)
			try:
				await self._data.do_update()
			except Exception as e:
				print(f"[ERROR]: Error while handling data updates: {e}")
				await self._data.emit_error(e)
			await (
				artificial_slow_down
			)  # uncomment to artificially slow down the update loop

	def stop_update_loop(self):
		self._signal_stop = True

	async def stop(self):
		self._signal_reload = False
		self.stop_update_loop()

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
		print("[INFO]: reloading system hub")
		self.stop_update_loop()
