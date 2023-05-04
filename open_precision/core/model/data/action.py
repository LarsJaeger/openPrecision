from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Any, Dict

from neomodel import UniqueIdProperty, StringProperty, StructuredNode, ArrayProperty, JSONProperty, Relationship

if TYPE_CHECKING:
    from open_precision.core.model.action_response import ActionResponse


class Action(StructuredNode):
    id: int = UniqueIdProperty()
    initiator: str = StringProperty(required=True)
    function_identifier: str = StringProperty(required=True)  # consists of the name of the class and the name
    # of the function separated by a dot; if a plugin should be accessed the format is plugins.<plugin_class_name>
    args: List[Any] = JSONProperty(required=True, default=list)
    kw_args: Dict[str, Any] = JSONProperty(required=True, default=dict)

    action_response: ActionResponse = Relationship('ActionResponse', 'RELATED_TO')
