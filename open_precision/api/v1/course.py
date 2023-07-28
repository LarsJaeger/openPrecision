from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter

from open_precision.api.utils import engine_endpoint
from open_precision.core.plugin_base_classes.navigator import Navigator

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub

course_router = APIRouter(
    prefix="/course",
    tags=["course"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@course_router.get("/")
@engine_endpoint
def _get_course(hub):
    return hub.plugins[Navigator].course


@course_router.post("/generate")
@engine_endpoint
def _generate_course(hub: SystemHub):
    hub.plugins[Navigator].set_course_from_course_generator()
    return hub.plugins[Navigator].course
