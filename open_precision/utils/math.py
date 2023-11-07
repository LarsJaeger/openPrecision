from __future__ import annotations

import math

import numpy as np
from numpy import linalg as la

from open_precision.core.model.location import Location


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


def angle_between_vectors(vector_a: np.array, vector_b: np.array):
    """returns angle between vector_a and vector_b as radian"""
    inner = np.inner(vector_a, vector_b)
    norms = la.norm(vector_a) * la.norm(vector_b)
    return np.arccos(np.divide(inner, norms))


def norm_vector(vec):
    return np.divide(
        vec, np.linalg.norm(vec), out=np.zeros_like(vec), where=np.linalg.norm(vec) != 0
    )


def calc_distance(loc1: Location, loc2: Location) -> float:
    return np.linalg.norm(loc2.to_numpy() - loc1.to_numpy())


def calc_distance_to_line(
        loc1: Location, line_base_point: Location, line_direction: np.array
) -> float:
    return np.divide(
        np.linalg.norm(np.cross((loc1 - line_base_point).to_numpy(), line_direction)),
        np.linalg.norm(line_direction),
    )


def intersections_of_circle_and_line_segment(
        point_translated_1: tuple[float, float],
        point_translated_2: tuple[float, float],
        circle_radius: float,
) -> list[tuple[float, float]]:
    # circle center is at (0,0)
    # calculation according to https://mathworld.wolfram.com/Circle-LineIntersection.html
    x_1, y_1 = point_translated_1
    x_2, y_2 = point_translated_2

    d_x = x_2 - x_1
    d_y = y_2 - y_1

    # Pre-compute variables common to x and y equations.
    d_r_squared = d_x ** 2 + d_y ** 2
    determinant = x_1 * y_2 - x_2 * y_1
    discriminant = circle_radius ** 2 * d_r_squared - determinant ** 2

    if discriminant < 0:
        raise ValueError("The line does not intersect the circle.")

    root = math.sqrt(discriminant)

    mp = np.array([-1, 1])  # Array to compute minus/plus.
    sign = -1 if d_y < 0 else 1

    coords_x = (determinant * d_y + mp * sign * d_x * root) / d_r_squared
    coords_y = (-determinant * d_x + mp * abs(d_y) * root) / d_r_squared

    candidate_1 = (coords_x[0], coords_y[0])
    candidate_2 = (coords_x[1], coords_y[1])

    # check if points are not only on line, but also on line segment and add if point is not already on list
    result = []
    if min(point_translated_1[0], point_translated_2[0]) <= candidate_1[0] <= max(
            point_translated_1[0], point_translated_2[0]
    ) and min(point_translated_1[1], point_translated_2[1]) <= candidate_1[1] <= max(
        point_translated_1[1], point_translated_2[1]
    ):
        # point 1 is on line -> add to list
        result.append(candidate_1)

    if (
            (
                    min(point_translated_1[0], point_translated_2[0])
                    <= candidate_2[0]
                    <= max(point_translated_1[0], point_translated_2[0])
            )
            and min(point_translated_1[1], point_translated_2[1])
            <= candidate_2[1]
            <= max(point_translated_1[1], point_translated_2[1])
            and candidate_1 != candidate_2
    ):
        # point 2 is on line and differs from point 1 -> add to list
        result.append(candidate_2)
    return result
