from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from neomodel import StructuredNode, UniqueIdProperty, Property, RelationshipTo, cardinality

from open_precision.core.model import DataModelBase

if TYPE_CHECKING:
    from open_precision.core.model.path import Path


@dataclass(kw_only=True)
class Course(StructuredNode, DataModelBase):
    id: str = UniqueIdProperty()
    name: str = Property(required=True)
    description: str = Property(required=False)

    CONTAINS: RelationshipTo = RelationshipTo('open_precision.core.model.path.Path',
                                              'CONTAINS',
                                              cardinality=cardinality.ZeroOrMore)

    def add_path(self, path: Path):
        self.CONTAINS.connect(path)
        return self
