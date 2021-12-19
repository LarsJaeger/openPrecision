import atexit
import numpy as np
from open_precision.core.model.vehicle import Vehicle


class VehicleManager:

    def __init__(self, manager):
        self._manager = manager
        self._manager.config.register_value(self, 'vehicles', [
            Vehicle(name='example_vehicle', gps_receiver_offset=np.ndarray([1, 2, 3]),
                    turn_radius_right=70.3, turn_radius_left=69.1)]) \
            .register_value(self, 'current_vehicle', 0)

        self._current_vehicle_id = self._manager.config.get_value(self, 'current_vehicle_id')
        self._vehicles = []
        self.load_data()
        atexit.register(self._cleanup())

    def _cleanup(self):
        self.save_data()

    def load_data(self):
        self._vehicles = self._manager.config.get_value(self, 'vehicles')
        self._current_vehicle_id = self._manager.config.get_value(self, 'current_vehicle_id')

    def save_data(self):
        self._manager.config.update_value(self, 'current_vehicle_id', self._current_vehicle_id) \
            .update_value(self, 'vehicles', self._vehicles)

    @property
    def current_vehicle(self) -> Vehicle:
        return self._vehicles[self._current_vehicle_id]

    @current_vehicle.setter
    def current_vehicle(self, new_vehicle_id: int):
        self._current_vehicle_id = new_vehicle_id

    @property
    def vehicles(self) -> list:
        return self._vehicles

    @vehicles.setter
    def vehicles(self, new_vehicles):
        self._vehicles = new_vehicles
