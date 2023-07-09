from __future__ import annotations

from dataclasses import dataclass

from neomodel import StructuredNode, JSONProperty, UniqueIdProperty

from open_precision.core.model import DataModelBase


class SystemConfiguration(DataModelBase, StructuredNode):
    """
    TODO: implement usage, add to model mapping list
    A system configuration consists of a vehicle and a list of sensors.
    """
    uuid: str = UniqueIdProperty()
    config: dict[str, str | list | dict] = JSONProperty(required=True)
