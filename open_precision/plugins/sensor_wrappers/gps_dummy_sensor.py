from open_precision.core.interfaces.sensor_types.global_positioning_system import GlobalPositioningSystem
from open_precision.core.managers.manager import Manager
from open_precision.core.model.location import Location


class GPSDummySensor(GlobalPositioningSystem):
    @property
    def location(self) -> Location:
        return Location(x=0, y=0, z=0, error=0)

    def __init__(self, manager: Manager):
        pass

    def cleanup(self):
        pass
