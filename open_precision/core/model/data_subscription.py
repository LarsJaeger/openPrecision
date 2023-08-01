import hashlib
from dataclasses import dataclass
from typing import Callable, Tuple, Any

import neomodel
from pydantic import BaseModel

from open_precision.core.model import DataModelBase
from open_precision.utils.neomodel import DillProperty


@dataclass(kw_only=True, frozen=True)
class DataSubscription(DataModelBase):
    func: Callable = None
    """
    TODO when remodelling the data subscriptions to persist throughout system restarts, __hash__ must use a subset of 
    func's properties (no session specific information, like place in memory).
    This could be done by creating a new property, compute it from func in __post_init__ and set hash=False for func. 
    """
    args: Tuple[Any, ...] = None
    kw_args: Tuple[Tuple[str, Any]] = None
    period_length: int = 0  # period length (minimum time between calling this func) in milliseconds

    def __hash__(self):
        return hash((self.func.__qualname__,
                     self.func.__code__,
                     self.func.__defaults__,
                     self.func.__kwdefaults__,
                     self.args,
                     self.kw_args,
                     self.period_length))

class DataSubscriptionProperty(DillProperty[DataSubscription], neomodel.Property):
    pass


class DataSubscriptionSchema(BaseModel):
    socket_id: str
    period_length: int = 0  # period length (minimum time between calling this func) in milliseconds
