from __future__ import annotations

import asyncio
import time as time_
from itertools import chain


def async_partial(f, *args):
    # source:
    # https://stackoverflow.com/questions/52422860/partial-asynchronous-functions-are-not-detected-as-asynchronous
    async def f2(*args2):
        result = f(*args, *args2)
        if asyncio.iscoroutinefunction(f):
            result = await result
        return result

    return f2


def is_iterable(obj: any):
    try:
        iterator = iter(obj)
    except TypeError:
        return False
    else:
        return True


def get_attrs_recursive(cls, excluded_classes: list[type] = None) -> set[str]:
    if excluded_classes is None:
        excluded_classes = []

    own_attrs = {attr for attr in cls.__dict__ if not attr.startswith('__')}
    if cls.__bases__:
        bases = [base for base in cls.__bases__ if base not in excluded_classes]
        return set(chain(*[get_attrs_recursive(base, excluded_classes) for base in bases], own_attrs))
    else:
        return own_attrs


def millis():
    return int(round(time_.time() * 1000))
