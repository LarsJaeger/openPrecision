import ruamel.yaml
from ruamel.yaml import YAML

import open_precision
from open_precision import utils


def _load_config_file(config_path):
    print('[LOG]: loading config file')
    with open(config_path) as config_file_stream:
        return YAML().load(stream=config_file_stream)


class ConfigManager:
    def __init__(self, config_path):
        self._config_path = config_path
        self.config = _load_config_file(self._config_path)
        self.classes = utils.get_classes_in_package('open_precision')
        print(self.classes)


ConfigManager('../../config.yml')
