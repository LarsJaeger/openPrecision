from neomodel import StructuredNode, UniqueIdProperty, RelationshipFrom, cardinality, RelationshipTo

from open_precision.core.model.data.data_model_base import DataModelBase


class Path(StructuredNode, DataModelBase):
    id: str = UniqueIdProperty()

    # incoming relationships

    REQUIRES: RelationshipFrom = RelationshipFrom('open_precision.core.model.data.path.Path',
                                                  'REQUIRES',
                                                  cardinality=cardinality.ZeroOrMore)

    CONTAINS: RelationshipFrom = RelationshipTo('open_precision.core.model.data.path.Path',
                                                'CONTAINS',
                                                cardinality=cardinality.ZeroOrMore)

    # outgoing relationships

    IS_CONTAINED_BY: RelationshipTo = RelationshipTo('open_precision.core.model.data.course.Course',
                                                     'CONTAINS',
                                                     cardinality=cardinality.ZeroOrMore)

    IS_REQUIRED_BY: RelationshipFrom = RelationshipFrom('open_precision.core.model.data.path.Path',
                                                        'REQUIRES',
                                                        cardinality=cardinality.ZeroOrMore)
