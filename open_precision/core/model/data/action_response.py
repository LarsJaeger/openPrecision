from __future__ import annotations

from neomodel import Relationship, UniqueIdProperty, StructuredNode, BooleanProperty, JSONProperty

from open_precision.core.model.data.action import Action


class ActionResponse(StructuredNode):

    id: str = UniqueIdProperty()
    action: Action = Relationship(Action, 'RELATED_TO')
    success: bool = BooleanProperty(required=True)
    response: str = JSONProperty(required=True)  # json of either the return value or the exception