from dataclasses import dataclass

from neomodel import StructuredNode, UniqueIdProperty, RelationshipFrom, cardinality, RelationshipTo

from open_precision.core.model import DataModelBase


@dataclass(kw_only=True)
class Path(StructuredNode, DataModelBase):
    id: str = UniqueIdProperty()

    # incoming relationships

    REQUIRES: RelationshipFrom = RelationshipFrom('open_precision.core.model.path.Path',
                                                  'REQUIRES',
                                                  cardinality=cardinality.ZeroOrMore)

    CONTAINS: RelationshipFrom = RelationshipTo('open_precision.core.model.waypoint.Waypoint',
                                                'CONTAINS',
                                                cardinality=cardinality.ZeroOrMore)

    # outgoing relationships

    IS_CONTAINED_BY: RelationshipTo = RelationshipTo('open_precision.core.model.course.Course',
                                                     'CONTAINS',
                                                     cardinality=cardinality.ZeroOrMore)

    IS_REQUIRED_BY: RelationshipFrom = RelationshipFrom('open_precision.core.model.path.Path',
                                                        'REQUIRES',
                                                        cardinality=cardinality.ZeroOrMore)
