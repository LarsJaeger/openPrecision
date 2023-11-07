from __future__ import annotations

import traceback
from typing import TYPE_CHECKING, Any, Callable

from aioprocessing import AioQueue, AioPipe

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class SystemTaskManager:
    """
    This class is used to queue and handle system tasks (func calls) to be executed in the main thread.

    ## Implementation details:
    queue_system_task(func, *args, **kwargs) queues a system task (func call) to be executed in the main thread. The
    passed func, args, kwargs, and the pipe end for sending the result put in a shared queue. When calling
    handle_tasks(amount) the given amount of tasks will be taken from the queue and executed in the main thread. The
    result will then be sent back through the pipe. Which triggers the queue_system_task func to return the result
    to its caller.
    """

    def __init__(self, manager: SystemHub):
        self._manager = manager
        self.task_queue = AioQueue()

    async def queue_system_task(
            self, func: Callable[[SystemHub], Any], *args, **kwargs
    ) -> Any:
        """
        Queues a system task (func call) to be executed in the main thread.
        :param func: func to be executed, must take a SystemHub as first argument, all other arguments must be
                     passed as args and kwargs
        :param args: positional arguments to be passed to func, must be serializable (dill)
        :param kwargs: keyword arguments to be passed to func, must be serializable (dill)
        :return: result of func
        """
        # create pipe
        pipe_out, pipe_in = AioPipe(duplex=False)
        # put action, args, kwargs and pipe in queue
        await self.task_queue.coro_put((func, args, kwargs, pipe_in))
        # wait for result
        await pipe_out.coro_poll()
        # return result
        ret = await pipe_out.coro_recv()
        # raise Exception if result is an exception
        if isinstance(ret, tuple) and isinstance(ret[0], Exception):
            print(ret[1])
            raise ret[0]
        return ret

    async def handle_tasks(self, amount: int = -1) -> None:
        """
        Executes the passed amount of tasks from the queue.
        :param amount: amount of tasks to execute;
            If amount is -1, tasks will be executed until the queue is empty. (default)
            If amount is 0, all currently queued tasks will be executed. (not the same as -1)
            Otherwise, the passed amount of tasks will be executed.

        :return: None
        """
        if amount == -1:
            while not self.task_queue.empty():
                await self.handle_tasks(0)

        elif amount == 0:
            amount = self.task_queue.qsize()

        for _ in range(amount):
            # skip if queue is empty
            if self.task_queue.empty():
                break

            # Get the func from the queue
            func, args, kwargs, conn = self.task_queue.get()
            # execute func
            try:
                ret = func(self._manager, *args, **kwargs)
            except Exception as e:
                ret = e, traceback.format_exc()
                print("Exception in system task: \n", str(e))
            # Send the result back
            with conn as conn:
                await conn.coro_send(ret)
