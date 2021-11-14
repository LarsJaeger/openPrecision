import atexit

from ruamel.yaml import YAML, CommentedMap, RoundTripLoader, RoundTripDumper
from open_precision import utils


# noinspection PyTypeChecker
class ConfigManager:
    def __init__(self, config_path: str):
        self._config: CommentedMap = None
        self._config_path = config_path
        self._load_config_file()
        self.classes = utils.get_classes_in_package('open_precision')
        """
        # check for new classes without config
        for any_class in self.classes:
            if any_class.__name__ not in self._config.keys():
                self._config[any_class.__name__] = None """
        atexit.register(self._cleanup)

    def _cleanup(self):
        self._save_config_file()

    def register_value(self, origin_object: object, value_name: str, value: any, comment: str = None):
        address = type(origin_object).__name__
        if value_name is not None:
            address += '.' + value_name
        self._pack_val(value, address.split(sep='.'), self._config, comment=comment)

    def get_value(self, origin_object: object, value_name: str):
        address = type(origin_object).__name__
        if value_name is not None:
            address += '.' + value_name
        return self._unpack_val(address.split(sep='.'), self._config)

    def _load_config_file(self):
        print('[LOG]: loading config file')
        with open(self._config_path) as config_file_stream:
            self._config = YAML().load(stream=config_file_stream)
        self._config = CommentedMap() if self._config is None else self._config

    def _save_config_file(self):
        print('[LOG]: saving config file')
        with open(self._config_path, 'r+') as config_file_stream:
            YAML().dump(self._config, stream=config_file_stream)

    def _unpack_val(self, list_address: list, config: CommentedMap):
        return config.get(list_address[0]) if len(list_address) == 1 else self._unpack_val(list_address[1:],
                                                                                       config[list_address[0]])

    def _pack_val(self, value, list_address: list, config: CommentedMap, comment: str = None):
        print('a' + str(list_address))
        print('a type' + str(config))
        print('b' + str(value))
        if len(list_address) == 1:
            if config.get(list_address[0]) is not None:
                config[list_address[0]] = value
            config.insert(0, list_address[0], value, comment=comment)
        else:
            if config.get(list_address[0]) is None:
                config.insert(0, list_address[0], CommentedMap())
            self._pack_val(value, list_address[1:], config.get(list_address[0]))
