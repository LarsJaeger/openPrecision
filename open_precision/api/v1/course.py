from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from open_precision.api.dependencies import queue_system_task_dependency
from open_precision.core.plugin_base_classes.navigator import Navigator

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub

course_router = APIRouter(
    prefix="/course",
    tags=["course"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def _get_course(hub):
    return hub.plugins[Navigator].course


@course_router.get("/")
async def get_course(queue_system_task=Depends(queue_system_task_dependency)):
    return JSONResponse(await queue_system_task(_get_course).to_json())


def _generate_course(hub: SystemHub):
    hub.plugins[Navigator].set_course_from_course_generator()
    return hub.plugins[Navigator].course


@course_router.post("/generate")
async def generate_course(queue_system_task=Depends(queue_system_task_dependency)):
    return JSONResponse(await queue_system_task(_generate_course))
