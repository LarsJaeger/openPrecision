import importlib
import inspect
from abc import ABC
from open_precision import utils


class SensorManager:

    def __init__(self, config):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.config = config
        self.plugin_dir = 'open_precision.plugins.sensor_adapters'
        self._sensor_types = utils.get_classes_in_package('open_precision.core.interfaces.sensor_types')
        print('found the following sensor types: ' + str(self.sensor_types))
        print(f'Looking for plugins under package {self.plugin_dir}')
        self._sensor_adapters = utils.get_classes_in_package(self.plugin_dir)
        print(f'found the following wrappers installed: {self._sensor_adapters}')
        self.available_sensors: tuple = (list(), list())
        self.check_sensor_availability()
        print(f'available sensors: {self.available_sensors}')

    def check_sensor_availability(self):
        self.available_sensors: tuple = (list(), list())
        for sensor_type_name, sensor_type in self.sensor_types:
            if sensor_type_name == 'BasicSensor':
                continue
            available_sensors_of_type = []
            for sensor_adapter_name, sensor_adapter in self._sensor_adapters:
                if issubclass(sensor_adapter, sensor_type) and sensor_adapter.is_available:
                    available_sensors_of_type.append(sensor_adapter)
            self.available_sensors[0].append(sensor_type)
            self.available_sensors[1].append(available_sensors_of_type)

    def get_sensor(self, sensor_type: any) -> any:
        print(self.available_sensors)
        if not isinstance(self.available_sensors[1][self.available_sensors[0].index(sensor_type)][0], type):
            self.available_sensors[1][self.available_sensors[0].index(sensor_type)][0].init(self.config)
        return self.available_sensors[1][self.available_sensors[0].index(sensor_type)][0]

    @property
    def sensor_types(self) -> tuple[str, any]:
        return self._sensor_types
