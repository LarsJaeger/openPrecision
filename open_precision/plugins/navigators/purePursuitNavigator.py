from math import sqrt

import numpy as np
from open_precision import utils
from open_precision.core.interfaces.navigator import Navigator
from open_precision.core.managers.manager import Manager
from open_precision.core.model.course import Course
from open_precision.core.model.position import Location, Position
from open_precision.core.model.waypoint import Waypoint
from open_precision.utils import intersections_of_circle_and_line_segment


class PurePursuitNavigator(Navigator):
    def __init__(self, manager: Manager):
        super().__init__(manager)
        self._manager = manager
        self._course: Course = None
        self._current_path_id = None

    @property
    def course(self):
        return self._course

    @course.setter
    def course(self, course: Course):
        self._course = course

    @property
    def _lookahead_distance(self):
        # TODO make dynamic
        return 10

    def get_steering_angle(self):
        current_position = self._manager.position_builder.current_position
        if self._current_path_id is None:
            # TODO get next(current) path
            # check priority
            # look for closest
            pass

        # get next waypoint of current path
        current_path_waypoints = self._course.paths[self._current_path_id].waypoints
        waypoint_base_id = None
        nearest_waypoint_distance = None
        for waypoint_id, waypoint in enumerate(current_path_waypoints):
            # check for the waypoint closest to lookahead
            if waypoint_base_id is None:
                waypoint_base_id = waypoint_id
                nearest_waypoint_distance = utils.calc_distance(current_position.location,
                                                                waypoint.location)
            else:
                waypoint_distance = utils.calc_distance(current_position.location,
                                                        waypoint.location)
                if waypoint_distance < nearest_waypoint_distance:
                    waypoint_base_id = waypoint_id
                    nearest_waypoint_distance = waypoint_distance

        # calculate which direction to go from waypoint_base (index positive changes, or index negative changes)
        if waypoint_base_id == 0:
            waypoint_target_id = 1
        elif waypoint_base_id == len(current_path_waypoints) - 1:
            waypoint_target_id = waypoint_base_id - 1
        else:
            # test if line from waypoint_id - 1 to waypoint_id or from waypoint_id to waypoint_id + 1 is the one
            # to follow
            if self.calc_line_error(current_position,
                                    current_path_waypoints[waypoint_base_id],
                                    current_path_waypoints[waypoint_base_id + 1]) \
                    > self.calc_line_error(current_position,
                                           current_path_waypoints[waypoint_base_id],
                                           current_path_waypoints[waypoint_base_id - 1]):
                waypoint_target_id = waypoint_base_id + 1
            else:
                waypoint_target_id = waypoint_base_id - 1
        path_direction_is_positive = True if (waypoint_target_id - waypoint_base_id) > 0 else False


        lookahead_distance = self._lookahead_distance
        # back rotation to rotate the important points from global to vehicle coordinate system
        global_to_vehicle = current_position.orientation.inverse

        target_point = None
        # walk through all waypoints in correct order
        for waypoint_id in range(waypoint_base_id + (1 if path_direction_is_positive else -1),
                                 len(current_path_waypoints) if path_direction_is_positive else 0):
            # determine if an intersection occurs between base waypoint and waypoint_id

            # determine possible intersections between lookahead circle and path line (infinitely long)
            # rotate to vehicle coordinates
            vec_base = global_to_vehicle \
                .rotate(current_path_waypoints[waypoint_id - (1 if path_direction_is_positive else -1)])
            vec_target = global_to_vehicle \
                .rotate(current_path_waypoints[waypoint_id])
            possible_target_points = intersections_of_circle_and_line_segment(vec_base[:1], vec_target[:1],
                                                                              lookahead_distance)
            #
            if len(possible_target_points) == 0:
                continue
            elif len(possible_target_points) == 2:
                # see which one is closer to vec_target
                d0 = sqrt(possible_target_points[0][0] ** 2 + possible_target_points[0][1] ** 2)
                d1 = sqrt(possible_target_points[1][0] ** 2 + possible_target_points[1][1] ** 2)
                if d0 < d1:
                    target_point = d0
                else:
                    target_point = d1
            else:
                target_point = possible_target_points[0]
            # target has been found -> break
            break
        if target_point is None:
            # i don't yet know what to do TODO think about solution
            return None

        # based on https://www.youtube.com/watch?v=qYR7mmcwT2w and http://www.davdata.nl/math/turning_radius.html
        # return result of formula arctan(W / (L² / (2*|gy|)))
        wheelbase = self._manager.vehicles.current_vehicle.wheelbase
        return np.arctan(wheelbase / ((lookahead_distance ** 2) / (2 * abs(target_point[1]))))

    def _calc_combined_error(self, offset_error: float, pos1, waypoint_base: Waypoint, waypoint_target: Waypoint):
        # rotation from global to vehicle reference system
        back_rotation = pos1.orientation.inverse
        # norm target_direction_vector
        target_direction_vector = utils.norm_vector(waypoint_target.location - waypoint_base.location)
        # calc *horizontal* heading error; horizon is a plane that has the vector of pos1 as a normal vector
        relative_orientation_vector = back_rotation.rotate(waypoint_target.location.to_numpy()) \
                                      - back_rotation.rotate(waypoint_base.location.to_numpy())

        """decide which turning radius to use (left or right):
        take direction vector of current waypoints, rotate it by the inverse of vehicle orientation and compare
        components to determine which way to turn"""
        heading_error = relative_orientation_vector[1] * (1 if relative_orientation_vector[0] < 0 else -1)
        if heading_error < 0:
            turning_radius = self._manager.vehicles.current_vehicle.turn_radius_right
        else:
            turning_radius = self._manager.vehicles.current_vehicle.turn_radius_left
        # calculate angle between vehicle direction and line direction
        heading_error_angle = np.arccos(np.clip(np.dot(relative_orientation_vector, np.ndarray([1, 0, 0])), -1.0, 1.0))
        # factor that describes the change of radius TODO make dependent on current speed
        speed_turning_radius_factor = 1.1
        # final_error = e_o + 1XX% r_min * (2 * e_h / pi)
        final_error = offset_error + np.multiply(np.multiply(speed_turning_radius_factor, turning_radius),
                                                 np.divide(heading_error_angle, np.pi))
        return final_error

    def calc_position_error(self, pos1: Position, target_location: Location,
                            target_direction_vector: np.ndarray) -> float:
        """ returns a value that becomes bigger the more effort it takes to reach a certain position. """
        # calculate offset:
        offset_error = utils.calc_distance(pos1.location, target_location)
        return self._calc_combined_error(offset_error, pos1, target_direction_vector)

    def calc_line_error(self, pos1: Position, waypoint_base: Waypoint, waypoint_target: Waypoint) -> float:
        """ returns a value that becomes bigger the more effort it takes to reach a certain position. """
        # calculate offset:
        offset_error = utils.calc_distance_to_line(pos1.location, waypoint_base.location,
                                                   waypoint_target.location.to_numpy())

        return self._calc_combined_error(offset_error, pos1, waypoint_base, waypoint_target)
