import inspect
import os
import time as time_
from datetime import datetime

import numpy as np


def millis():
    return int(round(time_.time() * 1000))


def get_rotation_matrix_ypr(y, p, r):
    """
    Rotationsmatrix für y=yaw, p=pitch, r=roll in degrees
    """
    # from Degree to Radians
    y = y * np.pi / 180.0
    p = p * np.pi / 180.0
    r = r * np.pi / 180.0

    rr = np.array([[1.0, 0.0, 0.0], [0.0, np.cos(r), -np.sin(r)], [0.0, np.sin(r), np.cos(r)]])
    rp = np.array([[np.cos(p), 0.0, np.sin(p)], [0.0, 1.0, 0.0], [-np.sin(p), 0.0, np.cos(p)]])
    ry = np.array([[np.cos(y), -np.sin(y), 0.0], [np.sin(y), np.cos(y), 0.0], [0.0, 0.0, 1.0]])

    return ry * rp * rr


def get_rotation_matrix_ypr_array(rotation_array: np.array) -> np.ndarray:
    """
    Rotationsmatrix für y=yaw, p=pitch, r=roll in degrees
    """
    # from Degree to Radians
    y = rotation_array[2] * np.pi / 180.0
    p = rotation_array[1] * np.pi / 180.0
    r = rotation_array[0] * np.pi / 180.0

    rr = np.array([[1.0, 0.0, 0.0], [0.0, np.cos(r), -np.sin(r)], [0.0, np.sin(r), np.cos(r)]])
    rp = np.array([[np.cos(p), 0.0, np.sin(p)], [0.0, 1.0, 0.0], [-np.sin(p), 0.0, np.cos(p)]])
    ry = np.array([[np.cos(y), -np.sin(y), 0.0], [np.sin(y), np.cos(y), 0.0], [0.0, 0.0, 1.0]])

    return np.dot(np.dot(ry, rp), rr)


def declination_from_vector(vector: np.array) -> float:
    # vector[0] -> forward; vector[1] -> left; vector[2] -> up
    return np.arctan(np.divide(vector[1], vector[0]))


def inclination_from_vector(vector: np.array) -> float:
    # vector[0] -> forward; vector[1] -> left; vector[2] -> up
    return np.arctan(np.divide(np.multiply(-1, vector[2]), vector[0]))


def get_classes_of_module(module):
    print("aa")
    for name, obj in inspect.getmembers(module):
        print("a")
        print(name)
        print(obj)
        if inspect.isclass(obj):
            print("b")
            print(obj)
