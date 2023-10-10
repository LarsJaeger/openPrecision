from __future__ import annotations

from typing import Callable, Any, Awaitable, TYPE_CHECKING

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub

# will be set by API class in __init__.py
_global_queue_task_func: Callable[[Callable[[SystemHub, ...], Any]], Awaitable[Any]] = None


async def queue_system_task_dependency():
    yield _global_queue_task_func
