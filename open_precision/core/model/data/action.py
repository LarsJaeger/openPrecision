from __future__ import annotations

from typing import TYPE_CHECKING, List, Any, Dict

from neomodel import UniqueIdProperty, StructuredNode, JSONProperty, Property, RelationshipFrom, cardinality

from open_precision.core.model.data.data_model_base import DataModelBase

if TYPE_CHECKING:
    pass


class Action(StructuredNode, DataModelBase):
    id: str = UniqueIdProperty()
    initiator: str = Property(required=True)
    function_identifier: str = Property(required=True)  # consists of the name of the class and the name
    # of the function separated by a dot; if a plugin should be accessed the format is plugins.<plugin_class_name>
    args: List[Any] = JSONProperty(required=True)
    kw_args: Dict[str, Any] = JSONProperty(required=True)

    RESPONDS_TO: RelationshipFrom = RelationshipFrom('open_precision.core.model.data.action_response.ActionResponse',
                                                     'RESPONDS_TO',
                                                     cardinality=cardinality.ZeroOrOne)
