from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from neomodel import StructuredNode, UniqueIdProperty, Property, RelationshipTo, cardinality, StringProperty

from open_precision.core.model import DataModelBase

if TYPE_CHECKING:
    from open_precision.core.model.path import Path

class Course(StructuredNode, DataModelBase):
    uuid: str = UniqueIdProperty()
    name: str = StringProperty(required=True)
    description: str = StringProperty(required=False)

    CONTAINS: RelationshipTo = RelationshipTo('open_precision.core.model.path.Path',
                                              'CONTAINS',
                                              cardinality=cardinality.ZeroOrMore)

    def add_path(self, path: Path):
        self.save()
        path.save()
        print("before connect")
        self.CONTAINS.connect(path)
        print("after connect")
        return self
