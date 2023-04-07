from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING
from open_precision.core.model.vehicle import Vehicle
from open_precision.managers.persistence_manager import PersistenceManager

if TYPE_CHECKING:
    from open_precision.manager import Manager


class VehicleManager:
    def __init__(self, manager: Manager):
        self._manager: Manager = manager
        self._manager.config.register_value(
            self,
            "vehicles",
            [
                {
                    "name": "example_vehicle",
                    "gps_receiver_offset": [1, 2, 3],
                    "turn_radius_right": 70.3,
                    "turn_radius_left": 69.1,
                    "wheelbase": 3.2,
                }
            ],
        ).register_value(self, "current_vehicle_id", 0)

        self._current_vehicle_id = self._manager.config.get_value(
            self, "current_vehicle_id"
        )
        self._vehicles = []
        self.load_data()

    def cleanup(self):
        self.save_data()

    def load_data(self):
        # init objects from config data

        # TODO remove after testing
        # print(f"soppp: {self._manager.config.get_value(self, 'vehicles')}")
        # self._vehicles: list[Vehicle] = [Vehicle(**kwargs) for kwargs in self._manager.config.get_value(self, "vehicles")]
        # print(f"supppp: {self._vehicles}")

        def make_vehicle_from_config_dict(conf_values: dict):
            obj = Vehicle()
            print("blub")
            print(obj)
            for key, value in conf_values.items():
                print("bla")
                print(type(value))
                print(value)
                setattr(obj, key, value)
            print("blub2")
            print(obj)
            return obj
        print("aaaaaaaa")
        print(type(self._manager.config.get_value(self, "vehicles")[0]))
        print(self._manager.config.get_value(self, "vehicles")[0])
        self._vehicles: list[Vehicle] = [make_vehicle_from_config_dict(x) for x in self._manager.config.get_value(self, "vehicles")]

        self._current_vehicle_id: int = self._manager.config.get_value(
            self, "current_vehicle_id"
        )

    def save_data(self):
        # Vehicle objects are converted to a dict before storing
        self._manager.config.set_value(
            self, "current_vehicle_id", self._current_vehicle_id
        ).set_value(self, "vehicles", [asdict(vehicle) for vehicle in self._vehicles])

    @property
    def current_vehicle(self) -> Vehicle:
        print(f"vehicles: {self._vehicles}")
        return self._vehicles[self._current_vehicle_id]

    @current_vehicle.setter
    @PersistenceManager.persist_arg
    def current_vehicle(self, new_vehicle_id: int):
        self._current_vehicle_id = new_vehicle_id

    @property
    def vehicles(self) -> list[Vehicle]:
        return self._vehicles

    @vehicles.setter
    @PersistenceManager.persist_arg
    def vehicles(self, new_vehicles: list[Vehicle]):
        self._vehicles = new_vehicles
