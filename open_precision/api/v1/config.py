from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from open_precision.api.dependencies import queue_system_task_dependency

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class ConfigSchema(BaseModel):
    content: str


config_router = APIRouter(
    prefix="/config",
    tags=["config"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@config_router.get("/")
async def get_config(queue_system_task=Depends(queue_system_task_dependency)) -> ConfigSchema:
    def get_config_inner(hub: SystemHub):
        return hub.config.get_config_string()

    config_string = await queue_system_task(get_config_inner)
    return ConfigSchema(content=config_string)


@config_router.put("/")
async def set_config(config: ConfigSchema, reload: bool = False,
                     queue_system_task=Depends(queue_system_task_dependency)):
    def set_config_inner(hub: SystemHub):
        hub.config.load_config(yaml=config.content, reload=reload)
        return hub.config.get_config_string()

    config_string = await queue_system_task(set_config_inner)
    return ConfigSchema(content=config_string)
