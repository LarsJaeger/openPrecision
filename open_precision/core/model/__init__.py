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
The annotation of class attribute show the datatype, the property type assigned to the attribute describes how the data type is stored.

## Data classes
Data classes that will not be explicitly stored as single nodes in the graph but can be stored as properties of nodes.
Every data class also needs a corresponding property class that maps the data class attributes to a neo4j supported data type.
These Property classes should be defined in the same module as the corresponding data class and must inherit from neomodel.Property (and implement the inflate and deflate methods).
The inflate method takes the value stored in the database and returns the data class, the deflate method takes the data class and returns the value that should be stored in the database.
"""
import json
from typing import List

import neomodel
from neomodel.properties import validator

signature_class_mapping = {}  # will be set by map_model function

class DataModelBase:
    def to_json(self):
        return CustomJSONEncoder().encode(self)

    @classmethod
    def signature(cls):
        """Used to identify the class in the CustomJSONDecoder"""
        return {attr for attr in list(dir(cls)) if not attr.startswith("__") and not attr.endswith("__")}


# extend the json.JSONEncoder class
class CustomJSONEncoder(json.JSONEncoder):

    # overload method default
    def default(self, obj):
        # Match all the types you want to handle in your converter
        if isinstance(obj, DataModelBase):
            return obj.to_json()

        return json.JSONEncoder.default(self, obj)


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        # TODO test
        # handle your custom classes
        if isinstance(obj, dict):
            keys = set(obj.keys())
            for signature, cls in signature_class_mapping:
                if signature == keys:
                    return cls(**obj)

        # handling the resolution of nested objects
        if isinstance(obj, dict):
            for key in list(obj):
                obj[key] = self.object_hook(obj[key])

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


def map_model():
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

    data_model_classes: List[DataModelBase] = [Action, ActionResponse, Course, Location, Orientation, Path, Position,
                                               Vehicle, VehicleState,
                                               Waypoint]
    for cls in data_model_classes:
        neomodel.install_labels(cls)
    # generate class signature mapping for deserialization of json to data model classes
    signature_class_mapping = {cls.signature(): cls for cls in data_model_classes}
