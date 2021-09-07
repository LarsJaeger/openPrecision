from open_precision import utils
from open_precision.core.exceptions import SensorNotConnectedError


def _group_sensors(sensor_types, sensor_adapters):
    _sensors: tuple = (list(), list())
    for sensor_type in sensor_types:
        if sensor_type.__name__ == 'BasicSensor':
            continue
        _sensors_of_type = []
        for sensor_adapter in sensor_adapters:
            if issubclass(sensor_adapter, sensor_type):
                _sensors_of_type.append(sensor_adapter)
        _sensors[0].append(sensor_type)
        _sensors[1].append(_sensors_of_type)
    return _sensors


def _initialise_sensors(available_sensors, config) -> dict:
    initialised_sensors = {}
    for sensor_type in available_sensors[0]:
        # initialises first class in sensor_adapter list of available_sensors
        try:
            initialised_sensors.update(
                {sensor_type: available_sensors[1][available_sensors[0].index(sensor_type)][0](config)})
        except SensorNotConnectedError:
            print(SensorNotConnectedError)
    return initialised_sensors


class SensorManager:

    def __init__(self, config):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.config = config
        self.plugin_dir = 'open_precision.plugins.sensor_wrappers'
        self._sensor_types = utils.get_classes_in_package('open_precision.core.interfaces.sensor_types')
        self._sensor_adapters = utils.get_classes_in_package(self.plugin_dir)
        print(f'found the following wrappers installed: {self._sensor_adapters}')
        self._grouped_sensors: tuple = _group_sensors(self.sensor_types, self._sensor_adapters)
        self._sensors = _initialise_sensors(self._grouped_sensors, config)

    @property
    def sensors(self):
        return self._sensors

    @property
    def sensor_types(self):
        return self._sensor_types
