from __future__ import annotations

from flatten_dict import flatten, unflatten
from ruamel.yaml import YAML, CommentedMap

from open_precision.managers import plugin_manager


class ConfigManager:
    def __init__(self, config_path: str):
        self._config: CommentedMap = CommentedMap()
        self._config_path = config_path
        self.load_config()
        self.classes = plugin_manager.get_classes_in_package("open_precision")
        for cls in self.classes:
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
        self._save_config_file()  # TODO possibly cache and save
        return self

    def get_value(self, origin_object: object, key: str) -> any:
        """returns value of key from origin_object's config"""
        address = type(origin_object).__name__
        if key is not None:
            address += "." + key
        flat_conf = flatten(self._config, reducer="dot")
        return (
            unflatten(flat_conf[address])
            if type(flat_conf[address]) is dict
            else flat_conf[address]
        )

    def cleanup(self):
        self._save_config_file()

    def load_config(self, yaml: str = None):
        """
        loads config file from yaml string or file
        :param yaml: if None, loads from file, else loads from this parameter (should be the yaml string)
        :return: None
        """
        print("[LOG]: loading config file")
        if yaml is None:
            with open(self._config_path) as config_file_stream:
                self._config = YAML().load(stream=config_file_stream)
        elif type(yaml) is str:
            self._config = YAML().load(yaml)
        else:
            raise TypeError("yaml must be None or str")
        self._config = CommentedMap() if self._config is None else self._config

    def _save_config_file(self):
        print("[LOG]: saving config file")
        with open(self._config_path, "w") as config_file_stream:
            YAML().dump(self._config, stream=config_file_stream)
