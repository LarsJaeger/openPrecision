import numpy as np
from open_precision import utils
from open_precision.core.interfaces.navigator import Navigator
from open_precision.core.managers.manager import Manager
from open_precision.core.model.course import Course
from open_precision.core.model.position import Location, Position
from open_precision.core.model.waypoint import Waypoint


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
            # TODO get next path
            # check priority
            # look for closest
            pass
        else:
            current_path_waypoints = self._course.paths[self._current_path_id].waypoints
            nearest_waypoint_id = None
            nearest_waypoint_distance = None
            for waypoint_id in range(len(current_path_waypoints)):
                # check for closest to lookahead
                if nearest_waypoint_id is None:
                    nearest_waypoint_id = waypoint_id
                    nearest_waypoint_distance = utils.calc_distance(current_position.location,
                                                                    current_path_waypoints[waypoint_id].location)
                else:
                    waypoint_distance = utils.calc_distance(current_position.location,
                                                            current_path_waypoints[waypoint_id].location)
                    if waypoint_distance < nearest_waypoint_distance:
                        nearest_waypoint_id = waypoint_id
                        nearest_waypoint_distance = waypoint_distance

            second_waypoint_id = None
            if nearest_waypoint_id == 0:
                second_waypoint_id = 1
            elif nearest_waypoint_id == len(current_path_waypoints) - 1:
                second_waypoint_id = nearest_waypoint_id - 1
            else:
                # test if line from waypoint_id - 1 to waypoint_id or from waypoint_id to waypoint_id + 1 is the one
                # to follow
                if self.calc_line_error(current_position,
                                        current_path_waypoints[nearest_waypoint_id],
                                        current_path_waypoints[nearest_waypoint_id + 1]) \
                        > self.calc_line_error(current_position,
                                               current_path_waypoints[nearest_waypoint_id],
                                               current_path_waypoints[nearest_waypoint_id - 1]):
                    second_waypoint_id = nearest_waypoint_id + 1
                else:
                    second_waypoint_id = nearest_waypoint_id - 1

        # TODO calc and return steering angle
        #   Maybe also save calc line errors from if statement in l 62 to not calc them again here
        # get next waypoint
        # return result of formula (2*|gy|) / L²
        return None

    def _calc_combined_error(self, offset_error: float, pos1, target_direction_vector: np.ndarray):
        # norm target_direction_vector
        target_direction_vector = utils.norm_vector(target_direction_vector)
        # calc *horizontal* heading error; horizon is a plane that has the vector of pos1 as a normal vector
        relative_orientation_vector = pos1.orientation.inverse.rotate(np.linalg.norm(target_direction_vector))

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

    def calc_line_error(self, pos1: Position, base_waypoint: Waypoint, target_waypoint: Waypoint) -> float:
        """ returns a value that becomes bigger the more effort it takes to reach a certain position. """
        # calculate offset:
        offset_error = utils.calc_distance_to_line(pos1.location, base_waypoint.location,
                                                   target_waypoint.location.to_numpy())

        # norm target_direction_vector
        target_direction_vector = utils.norm_vector((target_waypoint.location - base_waypoint.location).to_numpy())
        return self._calc_combined_error(offset_error, pos1, target_direction_vector)
