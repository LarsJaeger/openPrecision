from __future__ import annotations

from typing import TYPE_CHECKING

from neomodel import StructuredNode, UniqueIdProperty, RelationshipFrom, cardinality, RelationshipTo

from open_precision.core.model import DataModelBase

if TYPE_CHECKING:
    pass


class Path(StructuredNode, DataModelBase):

    uuid: str = UniqueIdProperty()

    # incoming relationships

    REQUIRES: RelationshipTo = RelationshipTo('open_precision.core.model.path.Path',
                                                  'REQUIRES',
                                                  cardinality=cardinality.ZeroOrMore)

    CONTAINS: RelationshipTo = RelationshipTo('open_precision.core.model.waypoint.Waypoint',
                                                'CONTAINS',
                                                cardinality=cardinality.ZeroOrMore)

    BEGINS_WITH: RelationshipFrom = RelationshipTo('open_precision.core.model.waypoint.Waypoint',
                                                   'BEGINS_WITH',
                                                   cardinality=cardinality.ZeroOrOne)

    ENDS_WITH: RelationshipFrom = RelationshipTo('open_precision.core.model.waypoint.Waypoint',
                                                 'ENDS_WITH',
                                                 cardinality=cardinality.ZeroOrOne)

    # outgoing relationships

    IS_CONTAINED_BY: RelationshipFrom = RelationshipFrom('open_precision.core.model.course.Course',
                                                     'CONTAINS',
                                                     cardinality=cardinality.ZeroOrMore)

    IS_REQUIRED_BY: RelationshipFrom = RelationshipFrom('open_precision.core.model.path.Path',
                                                        'REQUIRES',
                                                        cardinality=cardinality.ZeroOrMore)
