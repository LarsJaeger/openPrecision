from typing import TypeVar, Generic

import dill
import neomodel
from neomodel.properties import validator

T = TypeVar("T")


class DillProperty(neomodel.Property, Generic[T]):
	"""
	Property for storing data in a Neo4j database using dill serialization.
	"""

	@validator
	def inflate(self, value: str) -> T:
		return dill.loads(value)

	@validator
	def deflate(self, value: T) -> str:
		return dill.dumps(value)
