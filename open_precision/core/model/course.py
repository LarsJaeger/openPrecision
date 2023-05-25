from dataclasses import dataclass

from neomodel import StructuredNode, UniqueIdProperty, Property, RelationshipTo, cardinality

from open_precision.core.model import DataModelBase


@dataclass(kw_only=True)
class Course(StructuredNode, DataModelBase):
    id: str = UniqueIdProperty()
    name: str = Property(required=True)
    description: str = Property(required=False)

    CONTAINS: RelationshipTo = RelationshipTo('open_precision.core.model.data.course_element.CourseElement',
                                              'CONTAINS',
                                              cardinality=cardinality.ZeroOrMore)
