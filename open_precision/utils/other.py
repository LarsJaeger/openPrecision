from __future__ import annotations

import asyncio
import time as time_
from itertools import chain
from typing import Callable


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


def get_attributes(cls,
                   base_filter: Callable[[type], bool] = lambda x: True,
                   property_name_filter: Callable[[str], bool] = lambda x: True,
                   property_type_filter: Callable[[type], bool] = lambda x: True) -> set[str]:
    """
    Get all attributes of a class and its base classes recursively.
    :param cls:
    :param base_filter: function to filter base classes, inherited paths will be ignored above classes that do not pass the filter
    :param property_name_filter: function to filter property names, properties will be ignored if filter returns False
    :param property_type_filter: function to filter property types, properties will be ignored if filter returns False
    :return: a set of all property names of the class (including inherited ones)
    """

    own_attrs = {attr for attr, val in cls.__dict__.items() if property_name_filter(attr) and property_type_filter(val)}
    if cls.__bases__:
        bases = [base for base in cls.__bases__ if base_filter(base)]
        return set(chain(*[get_attributes(base, base_filter, property_name_filter, property_type_filter)
                           for base in bases],
                         own_attrs))
    else:
        return own_attrs


def millis():
    return int(round(time_.time() * 1000))
