from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from aioprocessing import AioQueue, AioPipe

if TYPE_CHECKING:
    from open_precision.manager_hub import ManagerHub


async def queue_func(queue: AioQueue, func: Callable[[ManagerHub], Any]) -> any:
    # create pipe
    pipe_out, pipe_in = AioPipe(duplex=False)
    # put action and pipe in queue
    await queue.coro_put((func, pipe_in))
    # wait for result
    await pipe_out.coro_poll()
    # return result
    return pipe_out.coro_recv()


class SystemTaskManager:
    def __init__(self, manager: ManagerHub):
        self._manager = manager
        self.task_queue = AioQueue()

    def queue_system_task(self, func: Callable[[ManagerHub], Any]) -> Any:
        return queue_func(self.task_queue, func)

    def handle_tasks(self, amount: int = -1) -> None:
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
                self.handle_tasks(0)
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
                ret = e
            # Send the result back
            with conn as conn:
                await conn.coro_send(ret)
