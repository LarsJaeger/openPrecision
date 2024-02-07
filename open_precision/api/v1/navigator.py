from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint
from open_precision.core.model.course import Course
from open_precision.core.model.path import Path
from open_precision.core.model.waypoint import Waypoint
from open_precision.core.plugin_base_classes.navigator import Navigator
from open_precision.core.plugin_base_classes.vehicle_state_builder import (
	VehicleStateBuilder,
)
from open_precision.plugins.course_generators.a_b_c_course_generator import (
	ABCCourseGenerator,
)
from open_precision.plugins.course_generators.a_heading_parallel_course_generator import (
	AHeadingParallelCourseGenerator,
)

if TYPE_CHECKING:
	from open_precision.system_hub import SystemHub

navigator_router = APIRouter(
	prefix="/navigator",
	tags=["navigator"],
	dependencies=[],
	responses={404: {"description": "Not found"}},
)


@navigator_router.get("/target_steering_angle")
@engine_endpoint
def get_target_steering_angle(hub) -> float:
	return hub.plugins[Navigator].target_machine_state.steering_angle


@navigator_router.post("/generate_course")
@engine_endpoint
def generate_course(hub: SystemHub, strategy: str = "AHeadingParallel"):
	if strategy == "AHeadingParallel":
		hub.plugins[
			Navigator
		].course = AHeadingParallelCourseGenerator.generate_course()
	elif strategy == "ABCParallel":
		hub.plugins[Navigator].course = ABCCourseGenerator.generate_course()
	course = hub.plugins[Navigator].current_course
	if course is None:
		return None
	return course.to_json(
		with_rels=[Course.CONTAINS, Path.CONTAINS, Waypoint.SUCCESSOR, Path.BEGINS_WITH]
	)


@navigator_router.get("/course")
@engine_endpoint
def get_current_course(hub: SystemHub):
	course = hub.plugins[Navigator].current_course
	if course is None:
		return None
	return course.to_json(
		with_rels=[Course.CONTAINS, Path.CONTAINS, Waypoint.SUCCESSOR, Path.BEGINS_WITH]
	)


@navigator_router.get("/current_path_id")
@engine_endpoint
def get_current_path_id(hub: SystemHub):
	return {"current_path_id": hub.plugins[Navigator].current_path_id}


@navigator_router.post("/set_path")
@engine_endpoint
def post_set_path(hub: SystemHub):
	hub.plugins[Navigator].set_path(hub.plugins[VehicleStateBuilder].current_position)
