from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from neomodel import StructuredNode, UniqueIdProperty, RelationshipFrom, cardinality, RelationshipTo, db

from open_precision.core.model import DataModelBase

if TYPE_CHECKING:
    from open_precision.core.model.waypoint import Waypoint


class Path(StructuredNode, DataModelBase):

    uuid: str = UniqueIdProperty()

    # incoming relationships

    REQUIRES: RelationshipTo = RelationshipTo('open_precision.core.model.path.Path',
                                                  'REQUIRES',
                                                  cardinality=cardinality.ZeroOrMore)

    CONTAINS: RelationshipTo = RelationshipTo('open_precision.core.model.waypoint.Waypoint',
                                                'CONTAINS',
                                                cardinality=cardinality.ZeroOrMore)

    # outgoing relationships

    IS_CONTAINED_BY: RelationshipFrom = RelationshipFrom('open_precision.core.model.course.Course',
                                                     'CONTAINS',
                                                     cardinality=cardinality.ZeroOrMore)

    IS_REQUIRED_BY: RelationshipFrom = RelationshipFrom('open_precision.core.model.path.Path',
                                                        'REQUIRES',
                                                        cardinality=cardinality.ZeroOrMore)

    @db.transaction
    def add_waypoint(self, waypoint: Waypoint):
        self.save()
        waypoint.save()
        self.CONTAINS.connect(waypoint)
        return self
