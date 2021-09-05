import importlib
import inspect
from abc import ABC
from open_precision import utils


class SensorManager:
    def __init__(self):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_dir = 'open_precision.plugins.sensor_adapters'
        print(f'Looking for plugins under package {self.plugin_dir}')
        self.installed_sensor_adapters = utils.get_classes_in_package(self.plugin_dir)
        print(f'found the following wrappers installed: {self.installed_sensor_adapters}')
        self.available_sensors: dict[str, list] = {}
        self.check_sensor_availability()
        print (f'available sensors: {self.available_sensors}')


    def check_sensor_availability(self):
        self.available_sensors: dict[str, list] = {}
        sensor_types = utils.get_classes_in_package('open_precision.core.interfaces.sensor_types')
        print(f'found the following sensor types: {sensor_types}')
        for (sensor_type_name, sensor_type) in sensor_types:
            if sensor_type_name == 'BasicSensor':
                break
            available_sensors_of_type = []
            for (sensor_adapter_name, sensor_adapter) in self.installed_sensor_adapters:

                if issubclass(sensor_adapter, sensor_type) and sensor_adapter.is_available():
                    available_sensors_of_type += sensor_adapter
            self.available_sensors.update({sensor_type, available_sensors_of_type})
