from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from starlette import status
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


@course_router.get("/")
async def get_course(queue_system_task=Depends(queue_system_task_dependency)):
    def get_course_inner(hub):
        return hub.plugins[Navigator].course

    course = await queue_system_task(get_course_inner)

    return JSONResponse(status_code=status.HTTP_200_OK, content=course.to_json())


@course_router.post("/generate")
async def generate_course(queue_system_task=Depends(queue_system_task_dependency)):
    def set_course_inner(hub: SystemHub):
        hub.plugins[Navigator].set_course_from_course_generator()
        return hub.plugins[Navigator].course

    course = await queue_system_task(set_course_inner)
    return JSONResponse(status_code=status.HTTP_200_OK, content=course.to_json())
