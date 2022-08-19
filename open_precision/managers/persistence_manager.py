from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, registry

from open_precision.core.model.persistence_model_base import PersistenceModelBase

if TYPE_CHECKING:
    from open_precision.manager import Manager


def subclasses_recursive(cls: type) -> list[type]:
    direct = cls.__subclasses__()
    indirect = []
    for subclass in direct:
        indirect.extend(subclasses_recursive(subclass))
    return direct + indirect


class PersistenceManager:

    @staticmethod
    def persist_return(func: callable) -> callable:
        """this decorator will persist the return value of the decorated function when it is called"""

        def wrapper(self, *args, **kwargs):
            val = func(self, *args, **kwargs)
            if isinstance(val, list):
                self._manager.persistence.save_objects(self, val)
            else:
                self._manager.persistence.save_object(self, val)
            return val

        return wrapper

    @staticmethod
    def persist_arg(func: callable) -> callable:
        """this decorator will persist the argument of the decorated function when it is called"""

        def wrapper(self, *args, **kwargs):
            val = args[0]
            if isinstance(val, list):
                self._manager._persistence.save_objects(self, val)
            else:
                self._manager._persistence.save_object(self, val)
            return func(self, *args, **kwargs)

        return wrapper

    def __init__(self, manager: Manager):
        self._manager = manager
        # init persistent relational db
        self._engine = create_engine('sqlite:///data.sqlite',
                                     echo=True)
        self._map_orm()
        self._session_maker = sessionmaker(bind=self._engine)
        self._session = self._session_maker()

    def _map_orm(self):
        mapper_registry = registry()
        # register every model class
        for cls in subclasses_recursive(PersistenceModelBase):
            print(f"[INFO]: mapping class {cls.__name__}")
            mapper_registry.mapped_as_dataclass(cls)
        mapper_registry.metadata.create_all(bind=self._engine)

    @staticmethod
    def _prep_for_db(origin_object: object, obj: PersistenceModelBase, parent: PersistenceModelBase = None) -> PersistenceModelBase:
        """prepares an object for the database"""
        if not isinstance(obj, PersistenceModelBase):
            raise TypeError(f"{obj} is not part of the persistence model")
        obj.last_updated = datetime.now()
        obj.last_updated_by = type(origin_object).__name__
        for attr_name in dir(obj):
            # check / run for every attribute of the object
            attr = getattr(obj, attr_name)
            if isinstance(attr, PersistenceModelBase):
                # in case attribute is not a list of objects
                if attr is not parent:
                    setattr(obj, attr_name, PersistenceManager._prep_for_db(origin_object, attr, obj))
            elif isinstance(attr, list):
                # in case attribute is a list of objects
                prepared_items = []
                for item in attr:
                    if item is not parent:
                        prepared_items.append(PersistenceManager._prep_for_db(origin_object, item, obj))
                    else:
                        prepared_items.append(item)
                setattr(obj, attr_name, prepared_items)
        return obj

    def get_object(self, origin_object: object, cls: type, id: int) -> PersistenceModelBase:
        """returns an object of type cls with id id"""
        session = self._session
        obj = session.query(cls).get(id)
        return obj

    def get_objects(self, origin_object: object, cls: type) -> list[PersistenceModelBase]:
        """returns all objects of type cls"""
        session = self._session
        objs = session.query(cls).all()
        return objs

    def save_object(self, origin_object: object, obj: PersistenceModelBase):
        """saves an object"""
        session = self._session
        session.add(self._prep_for_db(origin_object, obj))
        session.commit()

    def save_objects(self, origin_object: object, objs: list[PersistenceModelBase]):
        """saves a list of objects"""
        session = self._session
        for obj in objs:
            session.add(self._prep_for_db(origin_object, obj))
        session.commit()

    def delete_object(self, origin_object: object, obj: PersistenceModelBase):
        """deletes an object"""
        session = self._session
        session.delete(obj)
        session.commit()

    def delete_objects(self, origin_object: object, objs: list[PersistenceModelBase]):
        """deletes a list of objects"""
        session = self._session
        for obj in objs:
            session.delete(obj)
        session.commit()
