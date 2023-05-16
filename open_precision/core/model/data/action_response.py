from __future__ import annotations

from typing import TYPE_CHECKING

from neomodel import UniqueIdProperty, StructuredNode, JSONProperty, RelationshipTo, \
    Property, cardinality

from open_precision.core.model.data.data_model_base import DataModelBase

if TYPE_CHECKING:
    from open_precision.core.model.data.action import Action


class ActionResponse(StructuredNode, DataModelBase):
    id: str = UniqueIdProperty()
    success: bool = Property(required=True)
    response: any = JSONProperty(required=True)  # json of either the return value or the exception

    RESPONDS_TO: Action = RelationshipTo('open_precision.core.model.data.action.Action', 'RESPONDS_TO',
                                         cardinality=cardinality.ZeroOrOne)
