from datetime import datetime
import math
from open_precision.core.model.location import Location
from open_precision.core.plugin_base_classes.sensor_types.global_positioning_system import (
	GlobalPositioningSystem,
)
from open_precision.system_hub import SystemHub


class GPSDummySensor(GlobalPositioningSystem):
	@property
	def location(self) -> Location:
		time = datetime.now()
		return Location(
			x=3.0
			* math.sin(
				((float(time.second) + (float(time.microsecond) * 0.000001)) / 30.0)
				* math.pi
			),
			y=3.0
			* math.cos(
				((float(time.second) + (float(time.microsecond) * 0.000001)) / 30.0)
				* math.pi
			),
			z=0,
			error=0.01,
		)

	def __init__(self, manager: SystemHub):
		pass

	def cleanup(self):
		pass
