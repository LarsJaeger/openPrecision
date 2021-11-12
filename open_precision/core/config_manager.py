import atexit

from ruamel.yaml import YAML, CommentedMap
from open_precision import utils


# noinspection PyTypeChecker
class ConfigManager:
    def __init__(self, config_path: str):
        self._config: CommentedMap = None
        self._config_path = config_path
        self._load_config_file()
        self.classes = utils.get_classes_in_package('open_precision')
        # check for new classes without config
        for any_class in self.classes:
            if any_class.__name__ not in self._config.keys():
                self._config[any_class.__name__] = []
        atexit.register(self._cleanup)

    def _cleanup(self):
        self._save_config_file()

    def register_value(self, cls, value_name: str, value: any, comment: str = None):
        self._config.insert(1, cls.__name__, value, comment=comment)

    def get_value(self, cls, value_name: str):
        return self._config[cls.__name__][value_name]

    def get_config(self, cls):
        return self._config[cls.__name__]

    def _load_config_file(self):
        print('[LOG]: loading config file')
        with open(self._config_path) as config_file_stream:
            self._config = YAML().load(stream=config_file_stream)
        self._config = CommentedMap() if self._config is None else self._config

    def _save_config_file(self):
        print('[LOG]: saving config file')
        with open(self._config_path, 'r+') as config_file_stream:
            YAML().dump(self._config, stream=config_file_stream)
