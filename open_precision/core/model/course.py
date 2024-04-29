from __future__ import annotations

from typing import TYPE_CHECKING

from neomodel import (
	StructuredNode,
	UniqueIdProperty,
	RelationshipTo,
	cardinality,
	StringProperty,
	StructuredRel,
)

from open_precision.core.model import DataModelBase
from open_precision.core.model.relations.contains import Contains

if TYPE_CHECKING:
	from open_precision.core.model.path import Path


class Course(DataModelBase, StructuredNode):
	uuid: str = UniqueIdProperty()
	name: str = StringProperty(required=True)
	description: str = StringProperty(required=False)

	CONTAINS: RelationshipTo = RelationshipTo(
		"open_precision.core.model.path.Path",
		"CONTAINS",
		cardinality=cardinality.ZeroOrMore,
		model=Contains,
	)

	def add_path(self, path: Path):
		self.save()
		path.save()
		self.CONTAINS.connect(path)
		return self
