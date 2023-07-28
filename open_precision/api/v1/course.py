from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

import makefun as makefun
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


def engine_endpoint(func):
    func_sig = inspect.signature(func)
    params = list(func_sig.parameters.values())
    params.remove(params[0])  # remove hub
    params.insert(0, inspect.Parameter('queue_system_task',
                                       default=Depends(queue_system_task_dependency),
                                       kind=inspect.Parameter.POSITIONAL_OR_KEYWORD))
    new_sig = func_sig.replace(parameters=params)

    @makefun.wraps(func, new_sig=new_sig)
    async def endpoint(queue_system_task=Depends(queue_system_task_dependency), *args, **kwargs):
        return JSONResponse(await queue_system_task(func), *args, **kwargs)

    return endpoint


@course_router.get("/")
@engine_endpoint
def _get_course(hub):
    return hub.plugins[Navigator].course


"""
@course_router.get("/")
async def get_course(queue_system_task=Depends(queue_system_task_dependency)):
    return JSONResponse(await queue_system_task(_get_course).to_json())
"""


def _generate_course(hub: SystemHub):
    hub.plugins[Navigator].set_course_from_course_generator()
    return hub.plugins[Navigator].course


@course_router.post("/generate")
async def generate_course(queue_system_task=Depends(queue_system_task_dependency)):
    return JSONResponse(await queue_system_task(_generate_course))
