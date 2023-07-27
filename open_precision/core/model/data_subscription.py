from dataclasses import dataclass
from typing import Callable, Tuple, Any

from open_precision.core.model import DataModelBase
from open_precision.utils.neomodel import DillProperty


@dataclass(kw_only=True, frozen=True)
class DataSubscription(DataModelBase):
    function: Callable = None
    args: Tuple[Any, ...] = None
    kw_args: Tuple[Tuple[str, Any]] = None
    period_length: int = 0  # period length (minimum time between calling this function) in milliseconds


class DataSubscriptionProperty(DillProperty[DataSubscription]):
    pass
