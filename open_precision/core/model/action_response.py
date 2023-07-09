from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from neomodel import UniqueIdProperty, StructuredNode, JSONProperty, RelationshipTo, \
    Property, cardinality, BooleanProperty

from open_precision.core.model import DataModelBase

if TYPE_CHECKING:
    from open_precision.core.model.action import Action


class ActionResponse(StructuredNode, DataModelBase):
    uuid: str = UniqueIdProperty()
    success: bool = BooleanProperty(required=True)
    response: any = JSONProperty(required=True)  # json of either the return value or the exception

    RESPONDS_TO: Action = RelationshipTo('open_precision.core.model.action.Action', 'RESPONDS_TO',
                                         cardinality=cardinality.ZeroOrOne)
