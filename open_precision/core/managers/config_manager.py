import atexit

from flatten_dict import flatten, unflatten
from ruamel.yaml import YAML, CommentedMap
from open_precision import utils


class ConfigManager:
    def __init__(self, config_path: str):
        self._config: CommentedMap = CommentedMap()
        self._config_path = config_path
        self._load_config_file()
        self.classes = utils.get_classes_in_package('open_precision')
        atexit.register(self._cleanup)

    def register_value(self, origin_object: object, value_name: str, value: any) -> object:
        # YAML().register_class(type(value)) #register class

        address = type(origin_object).__name__
        if value_name is not None:
            address += '.' + value_name
        flat_conf = flatten(self._config, reducer='dot')
        if address not in flat_conf.keys():
            flat_conf[address] = value
        self._config = CommentedMap(unflatten(flat_conf, splitter='dot'))  # update config
        return self

    def set_value(self, origin_object: object, value_name: str, value: any) -> object:
        # YAML().register_class(type(value)) #register class

        address = type(origin_object).__name__
        if value_name is not None:
            address += '.' + value_name
        flat_conf = flatten(self._config, reducer='dot')
        flat_conf[address] = value
        self._config = CommentedMap(unflatten(flat_conf, splitter='dot'))
        return self

    def get_value(self, origin_object: object, value_name: str):
        address = type(origin_object).__name__
        if value_name is not None:
            address += '.' + value_name
        flat_conf = flatten(self._config, reducer='dot')
        return unflatten(flat_conf[address]) if type(flat_conf[address]) is dict else flat_conf[address]

    def _cleanup(self):
        self._save_config_file()

    def _load_config_file(self):
        print('[LOG]: loading config file')
        with open(self._config_path) as config_file_stream:
            self._config = YAML(typ='unsafe').load(stream=config_file_stream)
        self._config = CommentedMap() if self._config is None else self._config

    def _save_config_file(self):
        print('[LOG]: saving config file')
        with open(self._config_path, 'r+') as config_file_stream:
            YAML(typ='unsafe').dump(self._config, stream=config_file_stream)
