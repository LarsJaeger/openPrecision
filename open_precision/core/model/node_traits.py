from __future__ import annotations

from neomodel import StringProperty, db
from neomodel.contrib import SemiStructuredNode


class Storable(SemiStructuredNode):
	"""
	abstract base class for making Nodes storable by name
	"""

	name: str = StringProperty()

	def store(self, name):
		self.name = name
		self.save()

	def unstore(self):
		type(self).unstore(self.name)

	@classmethod
	def get_names(cls) -> List[str]:
		query = f"""
			MATCH (n:{cls.__qualname__})
			WHERE n.name IS NOT NULL
			RETURN n.name
		"""
		results, meta = db.cypher_query(query, {}, resolve_objects=True)
		return [res[0] for res in results]

	@classmethod
	def get(cls, name: str) -> Storable:
		query = f"""
			MATCH (n:{cls.__qualname__} {{name: $name}})
			WHERE n.name IS NOT NULL
			RETURN n.name
		"""
		results, meta = db.cypher_query(query, {"name": name}, resolve_objects=True)
		return results[0][0]

	@classmethod
	def unstore(cls, name: str):
		# TODO maybe delete if not connected to anything?
		query = f"""
			MATCH (n:{cls.__qualname__} {{name: $name}})
			REMOVE n.name
		"""
		results, meta = db.cypher_query(query, {"name": name}, resolve_objects=True)
