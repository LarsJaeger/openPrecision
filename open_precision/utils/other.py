from __future__ import annotations

import asyncio
import time as time_


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


def millis():
    return int(round(time_.time() * 1000))
