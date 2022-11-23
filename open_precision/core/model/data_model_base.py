import dataclasses
import json

from pyquaternion import Quaternion


def _todict_inner(obj, dict_factory=dict):
    # borrowed from module dataclasses with slight modifications
    if dataclasses._is_dataclass_instance(obj):
        result = []
        for f in dataclasses.fields(obj):
            if 'to_json' in list(obj.__dataclass_fields__[f.name].metadata.keys()) and not \
                    obj.__dataclass_fields__[f.name].metadata['to_json']:
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


class DataModelBase:
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        return _todict_inner(self)