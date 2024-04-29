from __future__ import annotations

from typing import TYPE_CHECKING

from neomodel import (
	UniqueIdProperty,
	StructuredNode,
	JSONProperty,
	RelationshipTo,
	cardinality,
	BooleanProperty,
)

from open_precision.core.model import DataModelBase
from open_precision.core.model.relations.responds_to import RespondsTo

if TYPE_CHECKING:
	from open_precision.core.model.action import Action


class ActionResponse(DataModelBase, StructuredNode):
	uuid: str = UniqueIdProperty()
	success: bool = BooleanProperty(required=True)
	response: any = JSONProperty(
		required=True
	)  # json of either the return value or the exception

	RESPONDS_TO: Action = RelationshipTo(
		"open_precision.core.model.action.Action",
		"RESPONDS_TO",
		cardinality=cardinality.ZeroOrOne,
		model=RespondsTo,
	)
