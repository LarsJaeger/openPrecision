from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import GlobalPositioningSystem
from open_precision.manager import Manager
from open_precision.core.model.data_classes.location import Location


class GPSDummySensor(GlobalPositioningSystem):
    @property
    def location(self) -> Location:
        return Location(x=0, y=0, z=0, error=None)

    def __init__(self, manager: Manager):
        pass

    def cleanup(self):
        pass
