from __future__ import annotations

from neomodel import UniqueIdProperty, cardinality, RelationshipFrom
from neomodel.contrib.semi_structured import SemiStructuredNode

from open_precision.core.model import DataModelBase
from open_precision.core.model.location import Location, LocationProperty
from open_precision.core.model.node_traits import Storable
from open_precision.core.model.relations.contains import Contains
from open_precision.core.model.relations.successor import Successor


class Waypoint(DataModelBase, Storable):
	uuid: str = UniqueIdProperty()
	location: Location = LocationProperty(required=True)

	# incoming relationships

	PREDECESSOR: RelationshipFrom = RelationshipFrom(
		"open_precision.core.model.waypoint.Waypoint",
		"SUCCESSOR",
		cardinality=cardinality.ZeroOrOne,
		model=Successor,
	)

	IS_CONTAINED_BY_PATH: RelationshipFrom = RelationshipFrom(
		"open_precision.core.model.path.Path",
		"CONTAINS",
		cardinality=cardinality.ZeroOrMore,
		model=Contains,
	)

	IS_CONTAINED_BY_COURSE: RelationshipFrom = RelationshipFrom(
		"open_precision.core.model.course.Course",
		"CONTAINS",
		cardinality=cardinality.ZeroOrMore,
		model=Contains,
	)

	# outgoing relationships

	SUCCESSOR: RelationshipFrom = RelationshipFrom(
		"open_precision.core.model.waypoint.Waypoint",
		"SUCCESSOR",
		cardinality=cardinality.ZeroOrOne,
		model=Successor,
	)
