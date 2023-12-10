from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from neomodel import Property
from neomodel.properties import validator

from open_precision.core.model import DataModelBase


@dataclass(kw_only=True)
class Location(DataModelBase):
	x: float = 0.0  # ECEF X coordinate in meters
	y: float = 0.0  # ECEF Y coordinate in meters
	z: float = 0.0  # ECEF Z coordinate in meters
	error: float | None = None  # position accuracy in meters

	def is_valid(self):
		return None not in [self.x, self.y, self.z]

	def __add__(self, other):
		match other:
			case Location():
				res_x = self.x + other.x
				res_y = self.y + other.y
				res_z = self.z + other.z
				if self.error is not None and other.error is not None:
					res_error = self.error + other.error
				else:
					res_error = None
			case list() | tuple():
				if (
					3 <= len(other) <= 4
					and self.error is not None
					and other[3] is not None
				):
					res_x = self.x + other[0]
					res_y = self.y + other[1]
					res_z = self.z + other[2]
				else:
					raise TypeError
				if len(other) == 4:
					res_error = self.error + other[3]
				else:
					res_error = None

			case np.ndarray():
				if 3 <= other.shape[0] <= 4:
					res_x = self.x + other[0]
					res_y = self.y + other[1]
					res_z = self.z + other[2]
				else:
					raise TypeError
				if len(other) == 4 and self.error is not None and other[3] is not None:
					res_error = self.error + other[3]
				else:
					res_error = None
			case _:
				raise TypeError
		return Location(x=res_x, y=res_y, z=res_z, error=res_error)

	def __sub__(self, other):
		match other:
			case Location():
				res_x = self.x - other.x
				res_y = self.y - other.y
				res_z = self.z - other.z
				if self.error is not None and other.error is not None:
					res_error = self.error + other.error
				else:
					res_error = None
			case list() | tuple():
				if 3 <= len(other) <= 4:
					res_x = self.x - other[0]
					res_y = self.y - other[1]
					res_z = self.z - other[2]
				else:
					raise TypeError
				if len(other) == 4 and self.error is not None and other[3] is not None:
					res_error = self.error - other[3]
				else:
					res_error = None

			case np.ndarray():
				if 3 <= other.shape[0] <= 4:
					res_x = self.x - other[0]
					res_y = self.y - other[1]
					res_z = self.z - other[2]
				else:
					raise TypeError
				if len(other) == 4 and self.error is not None and other[3] is not None:
					res_error = self.error + other[3]
				else:
					res_error = None
			case _:
				raise TypeError
		return Location(x=res_x, y=res_y, z=res_z, error=res_error)

	def to_numpy(self) -> np.array:
		return np.array([self.x, self.y, self.z], dtype=np.float64)


class LocationProperty(Property):
	"""
	A property that stores a Location object as a list of floats.
	"""

	@validator
	def inflate(self, value: list[float]) -> Location:
		return Location(
			x=value[0],
			y=value[1],
			z=value[2],
			error=value[3] if len(value) == 4 else None,
		)

	@validator
	def deflate(self, value: Location):
		if value.error is None:
			return [value.x, value.y, value.z]
		return [value.x, value.y, value.z, value.error]
