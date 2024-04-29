from __future__ import annotations

from typing import TYPE_CHECKING

from neomodel import (
	StructuredNode,
	UniqueIdProperty,
	RelationshipFrom,
	cardinality,
	RelationshipTo,
)
from open_precision.core import model

from open_precision.core.model import DataModelBase
from open_precision.core.model.relations.begins_with import BeginsWith
from open_precision.core.model.relations.contains import Contains
from open_precision.core.model.relations.ends_with import EndsWith
from open_precision.core.model.relations.requires import Requires

if TYPE_CHECKING:
	pass


class Path(DataModelBase, StructuredNode):
	uuid: str = UniqueIdProperty()

	# outgoing relationships

	REQUIRES: RelationshipTo = RelationshipTo(
		"open_precision.core.model.path.Path",
		"REQUIRES",
		cardinality=cardinality.ZeroOrMore,
		model=Requires,
	)

	CONTAINS: RelationshipTo = RelationshipTo(
		"open_precision.core.model.waypoint.Waypoint",
		"CONTAINS",
		cardinality=cardinality.ZeroOrMore,
		model=Contains,
	)

	BEGINS_WITH: RelationshipFrom = RelationshipTo(
		"open_precision.core.model.waypoint.Waypoint",
		"BEGINS_WITH",
		cardinality=cardinality.ZeroOrOne,
		model=BeginsWith,
	)

	ENDS_WITH: RelationshipFrom = RelationshipTo(
		"open_precision.core.model.waypoint.Waypoint",
		"ENDS_WITH",
		cardinality=cardinality.ZeroOrOne,
		model=EndsWith,
	)

	# incoming relationships

	IS_CONTAINED_BY: RelationshipFrom = RelationshipFrom(
		"open_precision.core.model.course.Course",
		"CONTAINS",
		cardinality=cardinality.ZeroOrMore,
		model=Contains,
	)

	IS_REQUIRED_BY: RelationshipFrom = RelationshipFrom(
		"open_precision.core.model.path.Path",
		"REQUIRES",
		cardinality=cardinality.ZeroOrMore,
	)
