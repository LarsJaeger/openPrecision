from __future__ import annotations

from typing import TYPE_CHECKING

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, registry

from open_precision.core.model.model_base import Model

if TYPE_CHECKING:
    from open_precision.manager import Manager


def subclasses_recursive(cls: type) -> list[type]:
    direct = cls.__subclasses__()
    indirect = []
    for subclass in direct:
        indirect.extend(subclasses_recursive(subclass))
    return direct + indirect


class DataManager:
    def __init__(self, manager: Manager):
        self._man = manager
        # init persistent relational db
        self._engine = create_engine('sqlite:///data.sqlite',
                                     echo=True)
        self._map_orm()
        self._session_maker = sessionmaker(bind=self._engine)

        # init in memory cache
        self._redis_session = redis.Redis(host='localhost', port=6379, db=0)

    def _map_orm(self):
        mapper_registry = registry()
        # register every model class
        for cls in subclasses_recursive(Model):
            mapper_registry.mapped(cls)

        mapper_registry.metadata.create_all(bind=self._engine)

    def _model_session(self) -> Session:
        """returns a new session to store model objects"""
        return self._session_maker()

    def _state_session(self):
        """returns a session to store the program state"""
        return self._redis_session


    def _model_get_object(self, cls: type, id: int) -> Model:
        """returns an object of type cls with id id"""
        session = self._model_session()
        obj = session.query(cls).get(id)
        session.close()
        return obj

    def _model_get_objects(self, cls: type) -> list[Model]:
        """returns all objects of type cls"""
        session = self._model_session()
        objs = session.query(cls).all()
        session.close()
        return objs

    def _model_save_object(self, obj: Model):
        """saves an object"""
        session = self._model_session()
        session.add(obj)
        session.commit()
        session.close()

    def _model_save_objects(self, objs: list[Model]):
        """saves a list of objects"""
        session = self._model_session()
        for obj in objs:
            session.add(obj)
        session.commit()
        session.close()

    def _model_delete_object(self, obj: Model):
        """deletes an object"""
        session = self._model_session()
        session.delete(obj)
        session.commit()
        session.close()

    def _model_delete_objects(self, objs: list[Model]):
        """deletes a list of objects"""
        session = self._model_session()
        for obj in objs:
            session.delete(obj)
        session.commit()
        session.close()


    def _state_get(self, key: str) -> str:
        """returns the value of key in the cache"""
        return self._redis_session.get(key)

    def _state_set(self, key: str, value: str):
        """sets the value of key in the cache"""
        self._redis_session.set(key, value)

    def _state_delete(self, key: str):
        """deletes the value of key in the cache"""
        self._redis_session.delete(key)

    def _clear_cache_keys(self, pattern: str):
        """clears all keys matching pattern in the cache"""
        self._redis_session.delete(*self._redis_session.scan_iter(match=pattern))

    def _clear_state(self):
        """clears the cache"""
        self._redis_session.flushdb()

