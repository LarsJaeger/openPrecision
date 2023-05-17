import dataclasses
import datetime
import json

from pyquaternion import Quaternion


def _todict_inner(obj, dict_factory=dict):
    # borrowed from module dataclasses with slight modifications
    if dataclasses._is_dataclass_instance(obj):
        result = []
        for f in dataclasses.fields(obj):
            if not obj.__dataclass_fields__[f.name].repr:
                continue
            value = _todict_inner(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).

        # I'm not using namedtuple's _asdict()
        # method, because:
        # - it does not recurse in to the namedtuple fields and
        #   convert them to dicts (using dict_factory).
        # - I don't actually want to return a dict here.  The main
        #   use case here is json.dumps, and it handles converting
        #   namedtuples to lists.  Admittedly we're losing some
        #   information here when we produce a json list instead of a
        #   dict.  Note that if we returned dicts here instead of
        #   namedtuples, we could no longer call asdict() on a data
        #   structure where a namedtuple was used as a dict key.

        return type(obj)(*[_todict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_todict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((_todict_inner(k, dict_factory),
                          _todict_inner(v, dict_factory))
                         for k, v in obj.items())
    elif isinstance(obj, Quaternion):
        obj = Quaternion()
        return {'x': obj.x, 'y': obj.y, 'z': obj.z, 'w': obj.w}
    else:
        return dataclasses.copy.deepcopy(obj)


def _json_defaults(obj) -> str:
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


class DataModelBase:
    def to_json(self):
        return json.dumps(self.to_dict(), default=_json_defaults)

    def to_dict(self) -> dict:
        return _todict_inner(self)

    @classmethod
    def from_json(cls, json_string: str):
        """creates a new instance of the class from a json string"""
        if json_string is None:
            raise TypeError('json_string must not be None')

        # do some manual assignments due to dataclasses not supporting initialization of inherited classes
        json_obj = json.loads(json_string)
        # remove all attrs that have an underscore attr (e.g. args is removed if _args exists)
        for key in json_obj.items():
            if key[0] == "_":
                json_obj.pop(key[1:])
        obj = cls()
        for key, value in json_obj.items():
            setattr(obj, key, value)
        return obj

    @classmethod
    def signature(cls):
        return {attr for attr in list(dir(cls)) if not attr.startswith("__") and not attr.endswith("__")}
