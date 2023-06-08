from __future__ import annotations

import traceback
from typing import TYPE_CHECKING, Any, Callable

from aioprocessing import AioQueue, AioPipe

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


async def queue_func(queue: AioQueue, func: Callable[[SystemHub], Any]) -> any:
    # create pipe
    pipe_out, pipe_in = AioPipe(duplex=False)
    # put action and pipe in queue
    await queue.coro_put((func, pipe_in))
    # wait for result
    await pipe_out.coro_poll()
    # return result
    ret = await pipe_out.coro_recv()
    # raise Exception if result is an exception
    if isinstance(ret, tuple) and isinstance(ret[0], Exception):
        print(ret[1])
        raise ret[0]
    return ret


class SystemTaskManager:
    def __init__(self, manager: SystemHub):
        self._manager = manager
        self.task_queue = AioQueue()

    async def queue_system_task(self, func: Callable[[SystemHub], Any]) -> Any:
        return await queue_func(self.task_queue, func)

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

            # Get the function from the queue
            func, conn = self.task_queue.get()
            # execute function
            try:
                ret = func(self._manager)
            except Exception as e:
                ret = e, traceback.format_exc()
            # Send the result back
            with conn as conn:
                await conn.coro_send(ret)
