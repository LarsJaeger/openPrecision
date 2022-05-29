from __future__ import annotations

import inspect
import os
import pkgutil
import time as time_
from cmath import cos
from math import sqrt

import numpy as np
import numpy.linalg as la

from open_precision.core.model.position import Location


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

    rr = np.array(
        [[1.0, 0.0, 0.0], [0.0, np.cos(r), -np.sin(r)], [0.0, np.sin(r), np.cos(r)]]
    )
    rp = np.array(
        [[np.cos(p), 0.0, np.sin(p)], [0.0, 1.0, 0.0], [-np.sin(p), 0.0, np.cos(p)]]
    )
    ry = np.array(
        [[np.cos(y), -np.sin(y), 0.0], [np.sin(y), np.cos(y), 0.0], [0.0, 0.0, 1.0]]
    )

    return ry * rp * rr


def get_rotation_matrix_ypr_array(rotation_array: np.array) -> np.array:
    """
    Rotationsmatrix für y=yaw, p=pitch, r=roll in degrees
    """
    # from Degree to Radians
    y = rotation_array[2] * np.pi / 180.0
    p = rotation_array[1] * np.pi / 180.0
    r = rotation_array[0] * np.pi / 180.0

    rr = np.array(
        [[1.0, 0.0, 0.0], [0.0, np.cos(r), -np.sin(r)], [0.0, np.sin(r), np.cos(r)]]
    )
    rp = np.array(
        [[np.cos(p), 0.0, np.sin(p)], [0.0, 1.0, 0.0], [-np.sin(p), 0.0, np.cos(p)]]
    )
    ry = np.array(
        [[np.cos(y), -np.sin(y), 0.0], [np.sin(y), np.cos(y), 0.0], [0.0, 0.0, 1.0]]
    )

    return np.dot(np.dot(ry, rp), rr)


def declination_from_vector(vector: np.array) -> float:
    # vector[0] -> forward; vector[1] -> left; vector[2] -> up
    return np.arctan(np.divide(vector[1], vector[0]))


def inclination_from_vector(vector: np.array) -> float:
    # vector[0] -> forward; vector[1] -> left; vector[2] -> up
    return np.arctan(np.divide(np.multiply(-1, vector[2]), vector[0]))


def get_classes_in_package(package: str) -> list:
    # returns a dict with classes as key and class names as value
    return _get_classes_in_package(package, [])


def _get_classes_in_package(package, classes: list) -> list:
    # recursively walk the supplied package to retrieve all classes
    imported_package = __import__(package, fromlist=["a"])

    for _, plugin_name, is_package in pkgutil.iter_modules(
            imported_package.__path__, imported_package.__name__ + "."
    ):
        if not is_package:
            plugin_module = __import__(plugin_name, fromlist=["a"])
            found_classes = inspect.getmembers(plugin_module, inspect.isclass)
            for name, cls in found_classes:
                if str(cls.__module__) == plugin_name:
                    classes.append(cls)

    # Now that we have looked at all the modules in the current package, start looking
    # recursively for additional modules in sub packages
    all_current_paths = []
    if isinstance(imported_package.__path__, str):
        all_current_paths.append(imported_package.__path__)
    else:
        all_current_paths.extend([x for x in imported_package.__path__])

    seen_paths = []
    for pkg_path in all_current_paths:
        if pkg_path not in seen_paths:
            seen_paths.append(pkg_path)

            # Get all sub directory of the current package path directory
            child_pkgs = [
                p
                for p in os.listdir(pkg_path)
                if os.path.isdir(os.path.join(pkg_path, p))
            ]

            # For each sub directory, apply the walk_package method recursively
            for child_pkg in child_pkgs:
                _get_classes_in_package(package + "." + child_pkg, classes)
    return classes


def angle_between_vectors(vector_a: np.array, vector_b: np.array):
    """returns angle between vector_a and vector_b as radian"""
    inner = np.inner(vector_a, vector_b)
    norms = la.norm(vector_a) * la.norm(vector_b)
    return np.arccos(np.divide(inner, norms))


def norm_vector(vec):
    return np.divide(
        vec, np.linalg.norm(vec), out=np.zeros_like(vec), where=np.linalg.norm(vec) != 0
    )


def calc_distance(loc1: Location, loc2: Location):
    return abs(loc2 - loc1)


def calc_distance_to_line(loc1: Location, line_base_point: Location, line_direction: np.ndarray):
    return np.divide(np.abs(np.cross(np.dot((loc1 - line_base_point).to_numpy())), line_direction),
                     np.abs(line_direction))


def intersections_of_circle_and_line_segment(point_on_line1: tuple[float] | list[float],
                                             point_on_line2: tuple[float] | list[float],
                                             circle_radius: float) -> list[tuple[float]]:
    # circle center is at (0,0)
    # calculation according to https://mathworld.wolfram.com/Circle-LineIntersection.html
    d_x = point_on_line2[0] - point_on_line1[0]  # delta x of line points
    d_y = point_on_line2[1] - point_on_line1[1]  # delta y of line points
    d_r = sqrt(d_x ** 2 + d_y ** 2)
    # here my understanding of the calculation stops
    d = point_on_line1[0] * point_on_line2[1] - point_on_line2[0] * point_on_line1[1]
    discriminant = (circle_radius ** 2) * (d_r ** 2) - (d ** 2)
    if discriminant < 0:
        return []
    # there is an intersection or tangent -> calculate points that are on line
    x_part1 = (d * d_y)
    x_part2 = ((1 if d_y < 0 else -1) * d_x * sqrt(discriminant))
    part3 = (d_r ** 2)
    x1_candidate = (x_part1 + x_part2) / part3
    x2_candidate = (x_part1 - x_part2) / part3
    y_part1 = (-d * d_x)
    y_part2 = (abs(d_y) * sqrt(discriminant))
    y1_candidate = (y_part1 + y_part2) / part3
    y2_candidate = (y_part1 - y_part2) / part3

    # check if points are not only on line, but also on line segment and add if point is not already on list
    result = []
    if min(point_on_line1[0], point_on_line2[0]) < x1_candidate < max(point_on_line1[0], point_on_line2[0]) \
            and min(point_on_line1[1], point_on_line2[1]) < y1_candidate < max(point_on_line1[1], point_on_line2[1]):
        # point 1 is on line -> add to list
        result.append((x1_candidate, y1_candidate))

    if (min(point_on_line1[0], point_on_line2[0]) < x2_candidate < max(point_on_line1[0], point_on_line2[0])) \
            and min(point_on_line1[1], point_on_line2[1]) < y2_candidate < max(point_on_line1[1], point_on_line2[1]) \
            and not all([x1_candidate == x2_candidate, y1_candidate == y2_candidate]):
        # point 2 is on line and differs from point 1 -> add to list
        result.append((x2_candidate, y2_candidate))
    return result
