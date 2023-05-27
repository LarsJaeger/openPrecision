from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

import neomodel
from neomodel import remove_all_labels

import open_precision.core.model as model
from open_precision.utils.other import is_iterable

if TYPE_CHECKING:
    from open_precision.managers.system_manager import SystemManager


class PersistenceManager:
    @staticmethod
    def persist_return(func: callable) -> callable:
        """this decorator will persist the return value of the decorated function when it is called"""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            val = func(self, *args, **kwargs)
            if is_iterable(val):
                [item.save() for item in val]
            else:
                val.save()
            return val

        return wrapper

    @staticmethod
    def persist_arg(func: callable, position_or_kw: int | str = 0) -> callable:
        """
        this decorator will persist the argument of the decorated function when it is called
        :param func: the function to decorate
        :param position_or_kw: the position or keyword of the argument to persist, defaults to 0
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if isinstance(position_or_kw, str):
                val = kwargs[position_or_kw]
            elif isinstance(position_or_kw, int):
                val = args[0]
            else:
                raise TypeError("position_or_kw must be either an int or a str")

            if is_iterable(val):
                [item.save() for item in val]
            else:
                val.save()
            return func(self, *args, **kwargs)

        return wrapper

    def __init__(self, manager: SystemManager):
        self._manager = manager

        neomodel.config.DATABASE_URL = 'neo4j+s://neo4j:SWDxmnOQ8hWgIvSbAue6mErmdMcDNXTZlYl0Rz6ZtjY@5852ce35.databases.neo4j.io'
        remove_all_labels()
        model.map_model()
