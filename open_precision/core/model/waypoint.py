from __future__ import annotations

from neomodel import StructuredNode, UniqueIdProperty, cardinality, RelationshipFrom

from open_precision.core.model import DataModelBase
from open_precision.core.model.location import Location, LocationProperty


class Waypoint(StructuredNode, DataModelBase):
    uuid: str = UniqueIdProperty()
    location: Location = LocationProperty(required=True)

    # incoming relationships

    PREDECESSOR: RelationshipFrom = RelationshipFrom('open_precision.core.model.waypoint.Waypoint',
                                                     'SUCCESSOR',
                                                     cardinality=cardinality.ZeroOrOne)

    IS_CONTAINED_BY_PATH: RelationshipFrom = RelationshipFrom('open_precision.core.model.path.Path',
                                                              'CONTAINS',
                                                              cardinality=cardinality.ZeroOrMore)

    IS_CONTAINED_BY_COURSE: RelationshipFrom = RelationshipFrom('open_precision.core.model.course.Course',
                                                                'CONTAINS',
                                                                cardinality=cardinality.ZeroOrMore)

    # outgoing relationships

    SUCCESSOR: RelationshipFrom = RelationshipFrom('open_precision.core.model.waypoint.Waypoint',
                                                   'SUCCESSOR',
                                                   cardinality=cardinality.ZeroOrOne)