from __future__ import annotations

from neomodel import StructuredNode, JSONProperty, UniqueIdProperty, ArrayProperty

from open_precision.core.model import DataModelBase
from open_precision.core.model.data_subscription import DataSubscriptionProperty


class SystemConfiguration(DataModelBase, StructuredNode):
    """
    TODO: implement usage, add to model mapping list
    A system configuration consists of a vehicle and a list of sensors.
    """
    uuid: str = UniqueIdProperty()
    config: dict[str, str | list | dict] = JSONProperty(required=True)
    data_subscriptions: list[str] = ArrayProperty(base_property=DataSubscriptionProperty, required=True)
