from __future__ import annotations

from math import sqrt

import numpy as np

from open_precision import utils
from open_precision.core.exceptions import CourseNotSetException
from open_precision.core.model.machine_state import MachineState
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.core.plugin_base_classes.position_builder import PositionBuilder
from open_precision.manager import Manager
from open_precision.core.model.course import Course
from open_precision.core.model.position import Position
from open_precision.core.model.location import Location
from open_precision.core.model.waypoint import Waypoint
from open_precision.managers.persistence_manager import PersistenceManager
from open_precision.utils import intersections_of_circle_and_line_segment


class PurePursuitNavigator(Navigator):
    def cleanup(self):
        pass

    def __init__(self, manager: Manager):
        super().__init__(manager)
        self._manager: Manager = manager
        self._course: Course | None = None
        self._current_path_id: int | None = None

    @property
    def course(self):
        return self._course

    @course.setter
    @PersistenceManager.persist_arg
    def course(self, course: Course):
        self._course = course
        
    @property
    @PersistenceManager.persist_return
    def target_machine_state(self) -> MachineState | None:
        target_machine_state = MachineState(steering_angle=self._steering_angle, speed=None)
        return target_machine_state

    @property
    def _lookahead_distance(self):
        # TODO make dynamic
        return 10

    @property
    def _steering_angle(self) -> float | None:
        # what's following now is a lot of spaghetti code
        if self._course is None:
            raise CourseNotSetException(self)
        current_position = self._manager.plugins[PositionBuilder].current_position
        waypoint_base_id = None

        if self._current_path_id is None:
            # look for closest
            best_segment_base_waypoint = None
            best_segment_target_waypoint = None
            smallest_loss = float('inf')
            for path_index, path in enumerate(self.course.paths):
                nr_of_waypoints = len(path.waypoints)
                for waypoint_id in range(nr_of_waypoints):
                    if waypoint_id == 0:
                        # check from wp_id 0 to wp_id 1
                        loss = self.calc_line_error(current_position, path.waypoints[0], path.waypoints[1])
                        if smallest_loss > loss:
                            smallest_loss = loss
                            best_path_id = path_index
                            best_segment_base_waypoint, best_base_id = path.waypoints[0], 0
                            best_segment_target_waypoint, best_target_id = path.waypoints[1], 1
                    elif waypoint_id == nr_of_waypoints - 1:
                        # check from wp_id nr_of_waypoints - 1 to previous wp
                        loss = self.calc_line_error(current_position, path.waypoints[nr_of_waypoints - 1],
                                                    path.waypoints[nr_of_waypoints - 2])
                        if smallest_loss > loss:
                            smallest_loss = loss
                            best_path_id = path_index
                            best_segment_base_waypoint, best_base_id = path.waypoints[nr_of_waypoints - 1], nr_of_waypoints - 1
                            best_segment_target_waypoint, best_target_id = path.waypoints[nr_of_waypoints - 2], nr_of_waypoints -2
                    else:
                        # check both directions
                        loss = self.calc_line_error(current_position, path.waypoints[waypoint_id],
                                                    path.waypoints[waypoint_id + 1])
                        if smallest_loss > loss:
                            smallest_loss = loss
                            best_path_id = path_index
                            best_segment_base_waypoint, best_base_id = path.waypoints[waypoint_id], waypoint_id
                            best_segment_target_waypoint, best_target_id = path.waypoints[waypoint_id + 1], waypoint_id + 1
                        loss = self.calc_line_error(current_position, path.waypoints[waypoint_id],
                                                    path.waypoints[waypoint_id - 1])
                        if smallest_loss > loss:
                            smallest_loss = loss
                            best_path_id = path_index
                            best_segment_base_waypoint, best_base_id = path.waypoints[waypoint_id], waypoint_id
                            best_segment_target_waypoint, best_target_id = path.waypoints[waypoint_id - 1], waypoint_id -1

            self._current_path_id = best_path_id
            waypoint_base_id = best_base_id
            path_direction_is_positive = best_base_id < best_target_id
            current_path_waypoints = best_segment_base_waypoint.path.waypoints
        else:
            # get next waypoint of current path
            current_path_waypoints = self._course.paths[self._current_path_id].waypoints
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
                """test if line from waypoint_id - 1 to waypoint_id or from waypoint_id to waypoint_id + 1 is the one
                to follow"""
                if self.calc_line_error(current_position,
                                        current_path_waypoints[waypoint_base_id],
                                        current_path_waypoints[waypoint_base_id + 1]) \
                        > self.calc_line_error(current_position,
                                               current_path_waypoints[waypoint_base_id],
                                               current_path_waypoints[waypoint_base_id - 1]):
                    waypoint_target_id = waypoint_base_id + 1
                else:
                    waypoint_target_id = waypoint_base_id - 1
            path_direction_is_positive = (waypoint_target_id - waypoint_base_id) > 0

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
            wp_base = current_path_waypoints[waypoint_id - (1 if path_direction_is_positive else -1)]
            vec_base = global_to_vehicle \
                .rotate(wp_base.location.to_numpy() - current_position.location.to_numpy())

            wp_target = current_path_waypoints[waypoint_id]
            vec_target = global_to_vehicle \
                .rotate(wp_target.location.to_numpy() - current_position.location.to_numpy())

            possible_target_points = intersections_of_circle_and_line_segment(vec_base[:2], vec_target[:2],
                                                                              lookahead_distance)
            match len(possible_target_points):
                case 0:
                    continue
                case 1:
                    target_point = possible_target_points[0]
                    # target has been found -> break
                    break
                case _:
                    # see which one is closer to vec_target
                    d0 = sqrt(possible_target_points[0][0] ** 2 + possible_target_points[0][1] ** 2)
                    d1 = sqrt(possible_target_points[1][0] ** 2 + possible_target_points[1][1] ** 2)
                    if d0 < d1:
                        target_point = d0
                    else:
                        target_point = d1
                    # target has been found -> break
                    break
        if target_point is None:
            # i don't yet know what to do TODO think about solution
            # print("target_point is none; no line in sight")
            return None

        # based on https://www.youtube.com/watch?v=qYR7mmcwT2w and http://www.davdata.nl/math/turning_radius.html
        # return result of formula arctan(W / (L² / (2*|gy|)))
        wheelbase = self._manager.vehicles.current_vehicle.wheelbase
        part1 = 2 * abs(target_point[1])
        part2 = lookahead_distance ** 2
        if part1 == 0 or part2 == 0:
            angle = 0
        else:
            angle = np.arctan(wheelbase / ((lookahead_distance ** 2) / (2 * abs(target_point[1]))))
        # set sign of angle dependent on turning direction
        angle = angle * (1 if target_point[1] < 0 else -1)
        return angle

    def _calc_combined_error(self, offset_error: float, pos1, waypoint_base: Waypoint, waypoint_target: Waypoint):
        # rotation from global to vehicle reference system
        back_rotation = pos1.orientation.inverse
        # norm target_direction_vector
        target_direction_vector = utils.norm_vector((waypoint_target.location - waypoint_base.location).to_numpy())
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
        heading_error_angle = np.arccos(np.clip(np.dot(relative_orientation_vector, np.array([1, 0, 0])), -1.0, 1.0))
        # factor that describes the change of radius TODO make dependent on current speed
        speed_turning_radius_factor = 1.1
        # final_error = e_o + 1XX% r_min * (2 * e_h / pi)
        final_error = offset_error + np.multiply(np.multiply(speed_turning_radius_factor, turning_radius),
                                                 np.divide(heading_error_angle, np.pi))
        return final_error

    def calc_position_error(self, pos1: Position, target_location: Location,
                            target_direction_vector: np.array) -> float:
        """ returns a value that becomes bigger the more effort it takes to reach a certain position. """
        # calculate offset:
        offset_error = utils.calc_distance(pos1.location, target_location)
        return self._calc_combined_error(offset_error, pos1, target_direction_vector)

    def calc_line_error(self, pos1: Position, waypoint_base: Waypoint, waypoint_target: Waypoint) -> float:
        """ returns a value that becomes bigger the more effort it takes to reach a certain position. """
        # calculate offset:
        offset_error = utils.calc_distance_to_line(pos1.location, waypoint_base.location,
                                                   (waypoint_target.location - waypoint_base.location).to_numpy())
        return self._calc_combined_error(offset_error, pos1, waypoint_base, waypoint_target)