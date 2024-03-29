from __future__ import annotations

import io
import traceback
from typing import TYPE_CHECKING

from flatten_dict import flatten, unflatten
from ruamel.yaml import YAML, CommentedMap
from ruamel.yaml.representer import RepresenterError

from open_precision.managers import plugin_manager

if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub


class ConfigManager:
	def __init__(self, manager: SystemHub):
		self._manager: SystemHub = manager
		self._config: CommentedMap = CommentedMap()
		self._config_path = self._manager._config_path
		self.load_config()
		self._classes = plugin_manager.get_classes_in_package("open_precision")
		for cls in self._classes:
			YAML().register_class(cls)  # register class

	def register_value(
		self, origin_object: object, key: str, value: any
	) -> ConfigManager:
		"""adds key/value pair to object's config if not already set"""

		address = type(origin_object).__name__
		if key is not None:
			address += "." + key
		flat_conf = flatten(self._config, reducer="dot")
		if address not in flat_conf.keys():
			flat_conf[address] = value
		self._config = CommentedMap(
			unflatten(flat_conf, splitter="dot")
		)  # update config
		return self

	def set_value(self, origin_object: object, key: str, value: any) -> ConfigManager:
		"""updates key's value in object's config"""
		address = type(origin_object).__name__
		if key is not None:
			address += "." + key
		flat_conf = flatten(self._config, reducer="dot")
		flat_conf[address] = value
		self._config = CommentedMap(unflatten(flat_conf, splitter="dot"))
		self.save_config_file()  # TODO possibly cache and save
		return self

	def get_value(self, origin_object: object, key: str) -> any:
		"""returns value of key from origin_object's config"""
		address = type(origin_object).__name__
		if key is not None:
			address += "." + key
		flat_conf = flatten(self._config, reducer="dot")
		return (
			unflatten(flat_conf[address])
			if isinstance(flat_conf[address], dict)
			else flat_conf[address]
		)

	def cleanup(self):
		self.save_config_file()

	def load_config(self, yaml: str = None, reload: bool = False):
		"""
		loads config file from yaml string or file
		:param reload: reinitializing backend after loading config if this is set to True
		:param yaml: if None, loads from file, else loads from this parameter (should be the yaml string)
		:return: None
		"""
		if yaml is None:
			print("[LOG]: loading config from file")
			try:
				with open(self._config_path, "r") as config_file_stream:
					self._config = YAML().load(stream=config_file_stream)
			except FileNotFoundError:
				print("[WARNING]: config file not found")
				self._config = CommentedMap()
		elif isinstance(yaml, str):
			print("[LOG]: loading config from string")
			self._config = YAML().load(yaml)
		else:
			raise TypeError("yaml must be None or str")
		self._config = CommentedMap() if self._config is None else self._config
		print("[DEBUG]: config: ", self._config)
		if reload:
			self._manager.reload()

	def save_config_file(self):
		print("[LOG]: saving config file")
		try:
			print("[DEBUG]: config: ", self._config)
			with open(self._config_path, "w") as config_file_stream:
				YAML().dump(self._config, stream=config_file_stream)
		except RepresenterError as e:
			print("[ERROR]: could not parse config file: ")
			print(self._config)
			print(" ".join(traceback.format_exception(e, value=e, tb=e.__traceback__)))
			return

	def get_config_string(self) -> str:
		try:
			config_buffer = io.StringIO()
			YAML().dump(self._config, stream=config_buffer)
			return config_buffer.getvalue()
		except RepresenterError as e:
			print("[ERROR]: could not parse config file: ")
			print(self._config)
			print(" ".join(traceback.format_exception(e, value=e, tb=e.__traceback__)))
			return ""
