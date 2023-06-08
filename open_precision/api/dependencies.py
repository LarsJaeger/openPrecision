_global_queue_task_func = None


async def queue_system_task_dependency():
    yield _global_queue_task_func
