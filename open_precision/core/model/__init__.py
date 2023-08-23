"""
model graph infrastructure:
https://arrows.app/#/import/json=eyJncmFwaCI6eyJzdHlsZSI6eyJmb250LWZhbWlseSI6InNhbnMtc2VyaWYiLCJiYWNrZ3JvdW5kLWNvbG9yIjoiI2ZmZmZmZiIsImJhY2tncm91bmQtaW1hZ2UiOiIiLCJiYWNrZ3JvdW5kLXNpemUiOiIxMDAlIiwibm9kZS1jb2xvciI6IiNmZmZmZmYiLCJib3JkZXItd2lkdGgiOjQsImJvcmRlci1jb2xvciI6IiMwMDAwMDAiLCJyYWRpdXMiOjUwLCJub2RlLXBhZGRpbmciOjUsIm5vZGUtbWFyZ2luIjoyLCJvdXRzaWRlLXBvc2l0aW9uIjoiYXV0byIsIm5vZGUtaWNvbi1pbWFnZSI6IiIsIm5vZGUtYmFja2dyb3VuZC1pbWFnZSI6IiIsImljb24tcG9zaXRpb24iOiJpbnNpZGUiLCJpY29uLXNpemUiOjY0LCJjYXB0aW9uLXBvc2l0aW9uIjoiaW5zaWRlIiwiY2FwdGlvbi1tYXgtd2lkdGgiOjIwMCwiY2FwdGlvbi1jb2xvciI6IiMwMDAwMDAiLCJjYXB0aW9uLWZvbnQtc2l6ZSI6NTAsImNhcHRpb24tZm9udC13ZWlnaHQiOiJub3JtYWwiLCJsYWJlbC1wb3NpdGlvbiI6Imluc2lkZSIsImxhYmVsLWRpc3BsYXkiOiJwaWxsIiwibGFiZWwtY29sb3IiOiIjMDAwMDAwIiwibGFiZWwtYmFja2dyb3VuZC1jb2xvciI6IiNmZmZmZmYiLCJsYWJlbC1ib3JkZXItY29sb3IiOiIjMDAwMDAwIiwibGFiZWwtYm9yZGVyLXdpZHRoIjo0LCJsYWJlbC1mb250LXNpemUiOjQwLCJsYWJlbC1wYWRkaW5nIjo1LCJsYWJlbC1tYXJnaW4iOjQsImRpcmVjdGlvbmFsaXR5IjoiZGlyZWN0ZWQiLCJkZXRhaWwtcG9zaXRpb24iOiJpbmxpbmUiLCJkZXRhaWwtb3JpZW50YXRpb24iOiJwYXJhbGxlbCIsImFycm93LXdpZHRoIjo1LCJhcnJvdy1jb2xvciI6IiMwMDAwMDAiLCJtYXJnaW4tc3RhcnQiOjUsIm1hcmdpbi1lbmQiOjUsIm1hcmdpbi1wZWVyIjoyMCwiYXR0YWNobWVudC1zdGFydCI6Im5vcm1hbCIsImF0dGFjaG1lbnQtZW5kIjoibm9ybWFsIiwicmVsYXRpb25zaGlwLWljb24taW1hZ2UiOiIiLCJ0eXBlLWNvbG9yIjoiIzAwMDAwMCIsInR5cGUtYmFja2dyb3VuZC1jb2xvciI6IiNmZmZmZmYiLCJ0eXBlLWJvcmRlci1jb2xvciI6IiMwMDAwMDAiLCJ0eXBlLWJvcmRlci13aWR0aCI6MCwidHlwZS1mb250LXNpemUiOjE2LCJ0eXBlLXBhZGRpbmciOjUsInByb3BlcnR5LXBvc2l0aW9uIjoib3V0c2lkZSIsInByb3BlcnR5LWFsaWdubWVudCI6ImNvbG9uIiwicHJvcGVydHktY29sb3IiOiIjMDAwMDAwIiwicHJvcGVydHktZm9udC1zaXplIjoxNiwicHJvcGVydHktZm9udC13ZWlnaHQiOiJub3JtYWwifSwibm9kZXMiOlt7ImlkIjoibjAiLCJwb3NpdGlvbiI6eyJ4IjotNC4xMjQzMzk0MDIzMjAxMDllLTMyLCJ5IjotMzAuNTYwOTQ5MjEyNTE5MDM0fSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJBY3Rpb24iXSwicHJvcGVydGllcyI6eyJpZCI6InN0ciIsImluaXRpYXRvciI6InN0ciIsImZ1bmN0aW9uX2lkZW50aWZpZXIiOiJzdHIiLCJhcmdzIjoiTGlzdFtBbnldIiwia3dfYXJncyI6IkRpY3Rbc3RyLCBBbnldIn0sInN0eWxlIjp7fX0seyJpZCI6Im4xIiwicG9zaXRpb24iOnsieCI6MCwieSI6MzAwfSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJBY3Rpb25fcmVzcG9uc2UiXSwicHJvcGVydGllcyI6eyJpZCI6InN0ciIsInN1Y2Nlc3MiOiJib29sIiwicmVzcG9uc2UiOiJzdHIifSwic3R5bGUiOnt9fSx7ImlkIjoibjIiLCJwb3NpdGlvbiI6eyJ4IjozMDAsInkiOi0zMC41NjA5NDkyMTI1MTkwMzR9LCJjYXB0aW9uIjoiIiwibGFiZWxzIjpbIkNvdXJzZSJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIiwibmFtZSI6InN0ciIsImRlc2NyaXB0aW9uIjoic3RyIn0sInN0eWxlIjp7fX0seyJpZCI6Im40IiwicG9zaXRpb24iOnsieCI6NjAwLCJ5IjoyMTguNDAxNTU5NzQxNjEzfSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJXYXlwb2ludCJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIiwibG9jYXRpb24iOiJMb2NhdGlvbiJ9LCJzdHlsZSI6e319LHsiaWQiOiJuNSIsInBvc2l0aW9uIjp7IngiOjQyMSwieSI6NDExfSwiY2FwdGlvbiI6IiIsImxhYmVscyI6WyJWZWhpY2xlIl0sInByb3BlcnRpZXMiOnsiaWQiOiJzdHIiLCJuYW1lIjoic3RyIiwidHVybl9yYWRpdXNfbGVmdCI6ImZsb2F0IiwidHVybl9yYWRpdXNfcmlnaHQiOiJmbG9hdCIsIndoZWVsYmFzZSI6ImZsb2F0IiwiZ3BzX3JlY2VpdmVyX29mZnNldCI6Ikxpc3RbZmxvYXRdIn0sInN0eWxlIjp7fX0seyJpZCI6Im43IiwicG9zaXRpb24iOnsieCI6NjMxLjY1MDE2MjM0NTczMzEsInkiOi0zMC41NjA5NDkyMTI1MTkwMzR9LCJjYXB0aW9uIjoiIiwic3R5bGUiOnt9LCJsYWJlbHMiOlsiUGF0aCJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIn19LHsiaWQiOiJuOCIsInBvc2l0aW9uIjp7IngiOjc0NywieSI6NjEyfSwiY2FwdGlvbiI6IiIsInN0eWxlIjp7fSwibGFiZWxzIjpbIlZlaGljbGVTdGF0ZSJdLCJwcm9wZXJ0aWVzIjp7ImlkIjoic3RyIiwic3RlZXJpbmdfYW5nbGUiOiJmbG9hdCIsInNwZWVkIjoiZmxvYXQiLCJwb3NpdGlvbiI6IlBvc2l0aW9uIn19XSwicmVsYXRpb25zaGlwcyI6W3siaWQiOiJuMCIsImZyb21JZCI6Im4wIiwidG9JZCI6Im4xIiwidHlwZSI6InJldHVybnMiLCJwcm9wZXJ0aWVzIjp7fSwic3R5bGUiOnt9fSx7ImlkIjoibjIiLCJ0eXBlIjoiU1VDQ0VTU09SIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjQiLCJ0b0lkIjoibjQifSx7ImlkIjoibjYiLCJ0eXBlIjoiQ09OVEFJTlMiLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuMiIsInRvSWQiOiJuNCJ9LHsiaWQiOiJuNyIsInR5cGUiOiJDT05UQUlOUyIsInN0eWxlIjp7fSwicHJvcGVydGllcyI6e30sImZyb21JZCI6Im4yIiwidG9JZCI6Im43In0seyJpZCI6Im44IiwidHlwZSI6IkNPTlRBSU5TIiwic3R5bGUiOnt9LCJwcm9wZXJ0aWVzIjp7fSwiZnJvbUlkIjoibjciLCJ0b0lkIjoibjQifSx7ImlkIjoibjkiLCJ0eXBlIjoiUkVRVUlSRVMiLCJzdHlsZSI6e30sInByb3BlcnRpZXMiOnt9LCJmcm9tSWQiOiJuNyIsInRvSWQiOiJuNyJ9XX0sImRpYWdyYW1OYW1lIjoiSW1wb3J0ZWQgZnJvbSBodHRwczovL3d3dy5hcGNqb25lcy5jb20vYXJyb3dzLyJ9


# The Model Implementation

The model consists of nodes and data classes (they **don't** need to be a dataclasses.dataclass)).
Both types of classes need to inherit from DataModelBase, which supplies serialization and deserialization methods.
All model classes must be in the data_model_classes list below.

## Nodes

Nodes are classes that inherit from StructuredNode. They are stored and queried in the graph database (neo4j).
To store them in the data base, use the .save() method of the object you want to store. To learn more about persistence,
look up the neomodel documentation.
The object graph mapper is neomodel, classes that should represent classes must inherit from neomodel.StructuredNode.
The annotation of class attribute show the datatype, the property type assigned to the attribute describes how the data
type is stored.
### Adding Nodes
To add a node, create a module with a class that inherits from neomodel.StructuredNode and DataModelBase, then add the class to the data_model_classes list in this module (the module import must happen in the map_model func).
The class attributes are the properties of the node.
The annotation of the class attribute shows the datatype of the property.
The value assigned to that attribute describes how the data type is stored and must be of neomodel.Property.
If the attribute should for example be data class as described below, the data class will be used in the type annotation, while the corresponding Property class will be used as the value assigned to the attribute.

## Data Classes
Data classes that won't be explicitly stored as single nodes in the graph but can be stored as properties of nodes.
Every data class also needs a corresponding property class that maps the data class attributes to a neo4j supported data type.
These Property classes should be defined in the same module as the corresponding data class and must inherit from neomodel.Property (and implement the inflate and deflate methods).
The inflate method takes the value stored in the database and returns the data class, the deflate method takes the data class and returns the value that should be stored in the database.

### Adding Data Classes
To add a data class, create a module with a class that inherits from DataModelBase and is decorated with dataclasses.dataclass(kw_only=True).
All attributes must have a value assigned to them in the class definition.
In that same module create a class that inherits from neomodel.Property and implement the inflate and deflate methods to inflate/deflate an object from/into a neo4j native type.


# JSON Serialization
Use the to_json method of DataModelBase objects or the CustomJSONEncoder class to serialize the object to json.
Use the from_json method of DataModelBase class or the CustomJSONDecoder class to deserialize the json string to an object.
The CustomJSONDecoder uses duck typing to determine the class of the object (more specifically, it uses the names of the class attributes (except relationships)).

Both serialization and deserialization ignore all relationships.
"""
from __future__ import annotations

import json
from functools import wraps
from types import FunctionType
from typing import List, Any, Callable

import neomodel
from neomodel import StructuredNode, RelationshipDefinition, RelationshipManager, RelationshipTo, RelationshipFrom
from neomodel.properties import validator
from pyquaternion import Quaternion

from open_precision.utils.other import get_attributes, is_iterable

signature_class_mapping: dict  # will be set by map_model func
class_signature_mapping: dict  # will be set by map_model func


def persist_return(func: callable) -> callable:
    """this decorator will persist the return value of the decorated func when it is called"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        val = func(self, *args, **kwargs)
        if is_iterable(val):
            [item.save() for item in val]
        else:
            val.save()
        return val

    return wrapper


def persist_arg(func: callable, position_or_kw: int | str = 0) -> callable:
    """
    this decorator will persist the argument of the decorated func when it is called
    :param func: the func to decorate
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


def _resolve_object_conns(obj: Any,
                          with_conns: List[RelationshipDefinition],
                          resolved_objects: List = None,
                          main_obj: Any = None,
                          ):
    connections = []
    objects = {}
    resolved_objects = resolved_objects if resolved_objects is not None else []

    if main_obj is None:  # only the case on the first recursion level
        main_obj = obj
        objects["main"] = main_obj
    else:
        objects[str(type(obj).__qualname__) + " " + str(obj.uuid)] = obj

    for field, value in obj.__dict__.items():
        if isinstance(value, RelationshipManager) and value.definition in with_conns:
            relationship = getattr(obj.__class__, field)

            if isinstance(relationship, RelationshipTo):
                rel_type = "to"
            elif isinstance(relationship, RelationshipFrom):
                rel_type = "from"
            else:
                rel_type = "undirected"

            # iterate over all connected objects and resolve their connections (recursion)
            for x in list(value):

                obj_a_ref: str = str(type(obj).__qualname__) + " " + str(obj.uuid) if obj != main_obj else "main"
                obj_b_ref: str = str(type(x).__qualname__) + " " + str(x.uuid) if x != main_obj else "main"
                connections.append({"a": obj_a_ref,
                                    "relationship": field,
                                    "type": rel_type,
                                    "b": obj_b_ref})

                if x in resolved_objects:  # prevent infinite recursion
                    continue
                resolved_objects.append(x)

                inner_objs, inner_conns = _resolve_object_conns(x,
                                                                with_conns=with_conns,
                                                                resolved_objects=resolved_objects,
                                                                main_obj=main_obj)
                objects.update(inner_objs)
                connections.extend(inner_conns)

    return objects, connections


class DataModelBase:
    def to_json(self,
                with_rels: List[RelationshipDefinition] = None,
                field_key_filter: Callable = None,
                field_type_filter: Callable = None,
                ) -> str:
        encoder = CustomJSONEncoder(field_type_filter=field_type_filter,
                                    field_key_filter=field_key_filter)
        if with_rels is None:
            return encoder.encode(self)
        else:
            objects, connections = _resolve_object_conns(self, [x.definition for x in with_rels])
            composite_object_dict = {"objects": objects,
                                     "connections": connections}
            return encoder.encode(composite_object_dict)

    @classmethod
    def from_json(cls, json_string: str, with_conns: bool = False):
        """
        Deserializes a json string to an object of the class. If the json string is a composite object (i.e. it contains
        connections), the main object is returned.
        If an object with the same uuid already exists in the database, it will be updated to have the properties of the
        serialized object and returned instead of a new object.

        :param json_string:
        :param with_conns:
        :return:
        """
        obj_dict = CustomJSONDecoder().decode(json_string)
        if obj_dict.keys() == {"objects", "connections"}:
            if with_conns:
                for obj in obj_dict["objects"].values():
                    obj.save()
                for conn in obj_dict["connections"]:
                    obj_a = obj_dict["objects"][conn["a"]]
                    obj_b = obj_dict["objects"][conn["b"]]
                    getattr(obj_a, conn["relationship"]).connect(obj_b)
            return obj_dict["objects"]["main"]
        else:
            return obj_dict


# extend the json.JSONEncoder class
class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self,
                 *args,
                 field_key_filter: Callable = None,
                 field_type_filter: Callable = None,
                 **kwargs):
        self.field_key_filter = field_key_filter if field_key_filter is not None else lambda x: True
        self.field_type_filter = field_type_filter if field_type_filter is not None else lambda x: True
        super().__init__(*args, **kwargs)

    # overload method default
    def default(self, obj):
        if isinstance(obj, DataModelBase):
            ret = {x: getattr(obj, x) for x in class_signature_mapping[obj.__class__]}
            ret = {k: v for k, v in ret.items() if self.field_key_filter(k) and self.field_type_filter(type(v))}
            return ret
        elif obj is None:
            return "null"
        elif isinstance(obj, Quaternion):
            return {"q": obj.q.tolist()}
        return json.JSONEncoder.default(self, obj)


class CustomJSONDecoder(json.JSONDecoder):
    """
    JSON decoder that is able to reconstruct subclasses of DataModelBase from JSON by matching keys with class attribute
    names. Relationship fields will be ignored.
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        # handling the resolution of nested objects
        if isinstance(obj, dict):
            keys_set = set(obj.keys())

            for key in keys_set:
                obj[key] = self.object_hook(obj[key])

            # check for quaternion
            if keys_set == {"q"}:
                return Quaternion(obj["q"])

            # check if the dict is a signature of a class
            for signature, cls in signature_class_mapping.items():
                if signature == keys_set:
                    if "uuid" in obj.keys():
                        ret = cls.nodes.get_or_none(uuid=obj["uuid"])
                        if ret is not None:
                            # update the object with the new values
                            for key, value in obj.items():
                                setattr(ret, key, value)
                            ret.save()

                            return ret
                    """
                    # remove relation information from dict
                    obj = {k: v for k, v in obj.items() if
                           not issubclass(type(getattr(cls, k)), RelationshipDefinition)}
                    """
                    return cls(**obj)
            else:
                return obj

        if isinstance(obj, list):
            for i in range(0, len(obj)):
                obj[i] = self.object_hook(obj[i])

            return obj

        return obj


class CustomJSONProperty(neomodel.JSONProperty):
    """
    Property for storing specific data types as JSON objects in Neo4j
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @validator
    def inflate(self, value: str) -> DataModelBase:
        return CustomJSONDecoder().decode(value)

    @validator
    def deflate(self, value: DataModelBase) -> str:
        return CustomJSONEncoder().encode(value)


def map_model(database_url: str):
    global signature_class_mapping, class_signature_mapping

    from open_precision.core.model.action import Action
    from open_precision.core.model.action_response import ActionResponse
    from open_precision.core.model.course import Course
    from open_precision.core.model.location import Location
    from open_precision.core.model.orientation import Orientation
    from open_precision.core.model.path import Path
    from open_precision.core.model.position import Position
    from open_precision.core.model.vehicle import Vehicle
    from open_precision.core.model.vehicle_state import VehicleState
    from open_precision.core.model.waypoint import Waypoint
    debug_url = "neo4j+s://neo4j:Qa89VmwaJINAYWqNm6ZYAWJFq8HXQB7LMH0UbZtFtkk@25c438c1.databases.neo4j.io:7687"
    neomodel.db.set_connection(database_url)  # database_url)

    data_model_classes: List[DataModelBase] = [Action, ActionResponse, Course, Location, Orientation, Path, Position,
                                               Vehicle, VehicleState, Waypoint]

    neomodel.remove_all_labels()
    for cls in data_model_classes:
        neomodel.install_labels(cls)

    # generate class signature mapping for deserialization of json to data model classes
    signature_class_mapping = {get_attributes(cls,
                                              base_filter=lambda x: x not in [DataModelBase, StructuredNode],
                                              property_name_filter=lambda x: (not x.startswith("_")) and (
                                                  x not in ["DoesNotExist", "id"] if issubclass(cls,
                                                                                                StructuredNode) else True),
                                              property_type_filter=lambda x: x is not FunctionType
                                                                             and not issubclass(x,
                                                                                                RelationshipDefinition))
                               : cls
                               for cls in data_model_classes}

    class_signature_mapping = {v: k for k, v in
                               signature_class_mapping.items()}  # reverse lookup table for signature_class_mapping

    print(class_signature_mapping)
