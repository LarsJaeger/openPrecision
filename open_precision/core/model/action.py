from __future__ import annotations

from typing import List, Any, Dict

from neomodel import (
	UniqueIdProperty,
	StructuredNode,
	JSONProperty,
	RelationshipFrom,
	cardinality,
	StringProperty,
)

from open_precision.core.model import DataModelBase


class Action(StructuredNode, DataModelBase):
	uuid: str = UniqueIdProperty()
	initiator: str = StringProperty(required=True)
	function_identifier: str = StringProperty(
		required=True
	)  # consists of the name of the class and the name
	# of the func separated by a dot; if a plugin should be accessed the format is plugins.<plugin_class_name>
	args: List[Any] = JSONProperty(required=True)
	kw_args: Dict[str, Any] = JSONProperty(required=True)

	RESPONDS_TO: RelationshipFrom = RelationshipFrom(
		"open_precision.core.model.action_response.ActionResponse",
		"RESPONDS_TO",
		cardinality=cardinality.ZeroOrOne,
	)
