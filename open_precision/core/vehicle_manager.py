import atexit
from pickle import Unpickler, Pickler

from open_precision.core.model.vehicle import Vehicle


class VehicleManager:

    def __init__(self, config):
        self.config = config
        self._current_vehicle = None
        self._vehicles = []
        self.load_data()
        atexit.register(self._cleanup())

    def _cleanup(self):
        self.save_data()

    def load_data(self):
        self._current_vehicle = Unpickler(self.config['current_vehicle_save_path']).load()
        self._vehicles = Unpickler(self.config['vehicles_save_path']).load()

    def save_data(self):
        Pickler(self.config['current_vehicle_save_path']).dump(self._current_vehicle)
        Pickler(self.config['vehicles_save_path']).dump(self._vehicles)

    @property
    def current_vehicle(self) -> Vehicle:
        return self._current_vehicle

    @current_vehicle.setter
    def current_vehicle(self, new_vehicle):
        self._current_vehicle = new_vehicle
