from __future__ import annotations

from math import sqrt

import numpy as np
from neomodel import db
from pyquaternion import Quaternion

import open_precision.utils.math
from open_precision.core.exceptions import CourseNotSetException
from open_precision.core.model import persist_arg
from open_precision.core.model.course import Course
from open_precision.core.model.location import Location
from open_precision.core.model.position import Position
from open_precision.core.model.vehicle_state import VehicleState
from open_precision.core.model.waypoint import Waypoint
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.core.plugin_base_classes.vehicle_state_builder import (
	VehicleStateBuilder,
)
from open_precision.system_hub import SystemHub
from open_precision.utils.math import intersections_of_circle_and_line_segment


class PurePursuitNavigator(Navigator):
	def cleanup(self):
		pass

	def __init__(self, manager: SystemHub):
		super().__init__(manager)
		self._manager: SystemHub = manager
		self._current_course: Course | None = None
		self._current_path_uuid: str | None = None
		self._is_segment_direction_positive: bool | None = None

	@property
	def current_course(self):
		return self._current_course

	@current_course.setter
	@persist_arg
	def current_course(self, course: Course):
		self._current_course = course

	@property
	def target_machine_state(self) -> VehicleState | None:
		target_machine_state = VehicleState(
			steering_angle=self._steering_angle, speed=None
		)
		return target_machine_state

	@property
	def _steering_angle(self) -> float | None:
		if self._current_course is None:
			raise CourseNotSetException(self)
		current_position = self._manager.plugins[VehicleStateBuilder].current_position
		waypoint_base: Waypoint | None = None
		waypoint_target: Waypoint | None = None

		# if current path is not set, find the closest path segment and set it
		if self._current_path_uuid is None:
			query = """
                    MATCH (:Course {uuid: $course_uuid})-[:CONTAINS]->(p:Path)-[:CONTAINS]->(w_a:Waypoint)-[:SUCCESSOR]->(w_b:Waypoint)
                    RETURN w_a, w_b, p.uuid
                    """
			results, meta = db.cypher_query(
				query, {"course_uuid": self._current_course.uuid}, resolve_objects=True
			)

			result_losses = [
				self.calc_line_error(current_position, wp_a, wp_b)
				for wp_a, wp_b, _ in results
			]
			inverted_results_losses = [
				self.calc_line_error(current_position, wp_b, wp_a)
				for wp_a, wp_b, _ in results
			]
			best_loss = min(result_losses)
			inverted_best_loss = min(inverted_results_losses)
			if best_loss < inverted_best_loss:
				waypoint_base, waypoint_target, self._current_path_uuid = results[
					result_losses.index(best_loss)
				]
				self._is_segment_direction_positive = True
			else:
				waypoint_base, waypoint_target, self._current_path_uuid = results[
					inverted_results_losses.index(inverted_best_loss)
				]
				self._is_segment_direction_positive = False

		# determine the target steering location

		lookahead_distance = 6  # TODO
		# back rotation to rotate the important points from global to vehicle coordinate system
		global_to_vehicle: Quaternion = current_position.orientation.inverse

		"""
        along the path in previously determined direction, check for intersections with lookahead circle, starting at 
        base waypoint query for waypoints with distance of w_a to current_position < lookahead_distance and w_b to
        current_position > lookahead_distance
        """

		query = """
                MATCH (:Course {uuid: $course_uuid})-[:CONTAINS]->(:Path{uuid: $path_uuid})-[:CONTAINS]->(w_a:Waypoint)-[:SUCCESSOR]->{1,}(w_b:Waypoint)
                RETURN w_a, w_b
                """
		results, meta = db.cypher_query(
			query,
			{
				"course_uuid": self._current_course.uuid,
				"path_uuid": self._current_path_uuid,
			},
			resolve_objects=True,
		)

		target_point = None
		current_location_np = current_position.location.to_numpy()
		# walk through all waypoints in correct order
		for waypoint_base, waypoint_target in results:
			# determine if an intersection occurs between base waypoint and waypoint_id

			# determine possible intersections between lookahead circle and path segment
			# rotate to vehicle coordinates
			vec_base = global_to_vehicle.rotate(
				waypoint_base.location.to_numpy() - current_location_np
			)

			vec_target = global_to_vehicle.rotate(
				waypoint_target.location.to_numpy() - current_location_np
			)

			possible_target_points = intersections_of_circle_and_line_segment(
				vec_base[:2], vec_target[:2], lookahead_distance
			)
			match len(possible_target_points):
				case 0:
					continue
				case 1:
					target_point = possible_target_points[0]
					# target has been found -> break
					break
				case _:
					# see which one is in the right direction
					if self._is_segment_direction_positive:
						path_end = vec_target
					else:
						path_end = vec_base

					p1 = possible_target_points[0]
					p2 = possible_target_points[1]

					d1 = sqrt((p1[0] - path_end[0]) ** 2 + (p1[1] - path_end[1]) ** 2)
					d2 = sqrt((p2[0] - path_end[0]) ** 2 + (p2[1] - path_end[1]) ** 2)

					if d1 < d2:
						target_point = p1
					else:
						target_point = p2
					# target has been found -> break
					break
		if target_point is None:
			# i don't yet know what to do TODO think about solution
			# print("target_point is none; no line in sight")
			return None

		# calculate steering angle based on target steering point
		# based on https://www.youtube.com/watch?v=qYR7mmcwT2w and http://www.davdata.nl/math/turning_radius.html
		# return result of formula arctan(W / (L² / (2*|gy|)))
		wheelbase = self._manager.vehicles.current_vehicle.wheelbase
		if target_point[1] == 0 or lookahead_distance == 0:
			angle = 0
		else:
			angle = np.arctan(
				wheelbase / ((lookahead_distance ** 2) / (2 * abs(target_point[1])))
			)
		# set sign of angle dependent on turning direction
		angle = angle * (1 if target_point[1] < 0 else -1)
		return angle

	def _calc_combined_error(
			self,
			offset_error: float,
			pos1,
			waypoint_base: Waypoint,
			waypoint_target: Waypoint,
	):
		# rotation from global to vehicle reference system
		back_rotation = pos1.orientation.inverse
		""""
		# norm target_direction_vector
		target_direction_vector = open_precision.utils.math.norm_vector(
			(waypoint_target.location - waypoint_base.location).to_numpy()
		)
		"""
		# calc *horizontal* heading error; horizon is a plane that has the vector of pos1 as a normal vector
		relative_orientation_vector = back_rotation.rotate(
			waypoint_target.location.to_numpy()
		) - back_rotation.rotate(waypoint_base.location.to_numpy())

		"""decide which turning radius to use (left or right):
        take direction vector of current waypoints, rotate it by the inverse of vehicle orientation and compare
        components to determine which way to turn"""
		heading_error = relative_orientation_vector[1] * (
			1 if relative_orientation_vector[0] < 0 else -1
		)
		if heading_error < 0:
			turning_radius = self._manager.vehicles.current_vehicle.turn_radius_right
		else:
			turning_radius = self._manager.vehicles.current_vehicle.turn_radius_left
		# calculate angle between vehicle direction and line direction
		heading_error_angle = np.arccos(
			np.clip(np.dot(relative_orientation_vector, np.array([1, 0, 0])), -1.0, 1.0)
		)
		# factor that describes the change of radius TODO make dependent on current speed
		speed_turning_radius_factor = 1.1
		# final_error = e_o + 1XX% r_min * (2 * e_h / pi)
		final_error = offset_error + np.multiply(
			np.multiply(speed_turning_radius_factor, turning_radius),
			np.divide(heading_error_angle, np.pi),
		)
		return final_error

	def calc_position_error(
			self,
			pos1: Position,
			target_location: Location,
			target_direction_vector: np.array,
	) -> float:
		"""returns a value that becomes bigger the more effort it takes to reach a certain position."""
		# calculate offset:
		offset_error = open_precision.utils.math.calc_distance(
			pos1.location, target_location
		)
		return self._calc_combined_error(offset_error, pos1, target_direction_vector)

	def calc_line_error(
			self, pos1: Position, waypoint_base: Waypoint, waypoint_target: Waypoint
	) -> float:
		"""returns a value that becomes bigger the more effort it takes to reach a certain position."""
		# calculate offset:
		offset_error = open_precision.utils.math.calc_distance_to_line(
			pos1.location,
			waypoint_base.location,
			(waypoint_target.location - waypoint_base.location).to_numpy(),
		)
		return self._calc_combined_error(
			offset_error, pos1, waypoint_base, waypoint_target
		)
