from __future__ import annotations

import atexit
import inspect
import os
import pkgutil
import traceback
from typing import TYPE_CHECKING

from open_precision.core.exceptions import PluginException, MissingPluginException

if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub


def get_classes_in_package(package, classes: list | None = None) -> list:
	if classes is None:
		classes = []

	# recursively walk the supplied package to retrieve all classes
	imported_package = __import__(package, fromlist=["a"])

	for _, plugin_name, is_package in pkgutil.iter_modules(
		imported_package.__path__, imported_package.__name__ + "."
	):
		if not is_package:
			try:
				plugin_module = __import__(plugin_name, fromlist=["a"])
				found_classes = inspect.getmembers(plugin_module, inspect.isclass)
				for name, cls in found_classes:
					if str(cls.__module__) == plugin_name:
						classes.append(cls)
			except ModuleNotFoundError:
				print(f"[INFO] ModuleNotFoundError when importing {plugin_name}")
				print(traceback.format_exc())
				continue

	# Now that we have looked at all the modules in the current package, start looking recursively for additional
	# modules in sub packages
	all_current_paths = []
	if isinstance(imported_package.__path__, str):
		all_current_paths.append(imported_package.__path__)
	else:
		all_current_paths.extend([x for x in imported_package.__path__])

	seen_paths = []
	for pkg_path in all_current_paths:
		if pkg_path not in seen_paths:
			seen_paths.append(pkg_path)

			# Get all subdirectory of the current package path directory
			child_pkgs = [
				p
				for p in os.listdir(pkg_path)
				if os.path.isdir(os.path.join(pkg_path, p))
			]

			# For each subdirectory, apply the get_classes_in_package method recursively
			for child_pkg in child_pkgs:
				get_classes_in_package(package + "." + child_pkg, classes)
	return classes


def _check_plugins_for_class(plugin_class, plugins) -> list:
	"""returns all plugins that are a subclass of plugin_class"""

	checked_plugins = []
	for plugin in plugins:
		if issubclass(plugin, plugin_class):
			checked_plugins.append(plugin)
	return checked_plugins


class PluginManager:
	def __init__(
		self, manager: SystemHub, plugin_type_class: type, plugin_package: str
	):
		atexit.register(self._cleanup)
		self._manager: SystemHub = manager
		self._plugin_type_class: type = plugin_type_class
		self._plugin_package: str = plugin_package
		self._manager.config.register_value(
			self, f"loading_priority.{self._plugin_type_class.__name__}", []
		)
		print(
			f"[ClassPluginManager] loading plugins for type: {str(self._plugin_type_class.__name__)}"
		)
		self._plugin_instance: any = self._initialise_plugin()
		print(
			f"[ClassPluginManager] initialised plugin: {str(self._plugin_instance.__class__)}"
		)
		print(
			f"[ClassPluginManager] finished loading plugins for type: {str(self.plugin_type_class.__name__)}"
		)

	def _cleanup(self) -> None:
		pass

	def _initialise_plugin(self) -> any:
		# get possible plugins
		plugins = get_classes_in_package(self._plugin_package, [])
		possible_plugins = _check_plugins_for_class(self._plugin_type_class, plugins)
		# get plugin loading priority
		plugin_loading_priority = self._manager.config.get_value(
			self, f"loading_priority.{self._plugin_type_class.__name__}"
		)
		for plugin in possible_plugins:
			if plugin.__name__ not in plugin_loading_priority:
				plugin_loading_priority.append(plugin.__name__)
		# save back to config
		self._manager.config.set_value(
			self,
			f"loading_priority.{self._plugin_type_class.__name__}",
			plugin_loading_priority,
		)

		# create reverse lookup table
		plugins_from_name = {plugin.__name__: plugin for plugin in possible_plugins}

		# initialises first initialisable class from plugin loading priority
		if possible_plugins is None:
			raise MissingPluginException(
				str(self._plugin_type_class), self._plugin_package
			)
		for current_init_plugin in plugin_loading_priority:
			try:
				return plugins_from_name[current_init_plugin](self._manager)
			except PluginException:
				print(
					f"[ERROR] Aborting! An error occurred while enabling {current_init_plugin}: {str(PluginException)}"
				)
				traceback.print_exc()
			except:  # noqa
				print(
					f"[ERROR] Aborting! An error occurred while enabling {current_init_plugin}."
				)
				traceback.print_exc()

	@property
	def instance(self):
		return self._plugin_instance

	@property
	def plugin_type_class(self):
		return self._plugin_type_class
