from __future__ import annotations

from neomodel import StructuredNode, JSONProperty, UniqueIdProperty

from open_precision.core.model import DataModelBase


class SystemConfiguration(DataModelBase, StructuredNode):
	"""
	TODO: implement usage, add to model mapping list
	A system configuration consists of a vehicle and a list of sensor.
	"""

	uuid: str = UniqueIdProperty()
	config: dict[str, str | list | dict] = JSONProperty(required=True)


# data_subscriptions: list[DataSubscription] = ArrayProperty(base_property=DataSubscriptionProperty, required=True)
