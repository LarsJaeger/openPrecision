from datetime import datetime

from open_precision.core.model.location import Location
from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import GlobalPositioningSystem
from open_precision.system_hub import SystemHub


class GPSDummySensor(GlobalPositioningSystem):
    @property
    def location(self) -> Location:
        # 0 0 0 for the first 10 seconds, then 1 1 1
        if (datetime.now() - self._init_time).total_seconds() > 100:
            return Location(x=4179284.0, y=735289.0, z=4746380.0)
        return Location(x=0, y=0, z=0)

    def __init__(self, manager: SystemHub):
        self._init_time = datetime.now()
        pass

    def cleanup(self):
        pass
