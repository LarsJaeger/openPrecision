from __future__ import annotations

import inspect
from json import JSONEncoder
from typing import Callable, Any

import makefun
from fastapi import Depends
from starlette.responses import JSONResponse

from open_precision.api import dependencies as dependencies
from open_precision.core.model import DataModelBase
from open_precision.core.model.data_subscription import DataSubscriptionSchema, DataSubscription
from open_precision.system_hub import SystemHub


def engine_endpoint(func: Callable[[SystemHub, ...], Any]) -> Callable[[...], Any]:
    """
    Decorator to make fastapi endpoint functions from functions that need to be run in the engine (update loop in the
    main thread).

    The decorated function must have a variable of type SystemHub as their first positional argument.
    The following arguments can be treated as if the function was a FastAPI endpoint function, however it must still be
    decorated as such!
    The Endpoint will return the returned value from the engine function as JSON. The status code of the returned JSON
    will either be 200 (default), or 500 (if an error occured while executing the function).

    Usage:
    ```python
    @app.post("/generate{foo}")
    @engine_endpoint
    def _generate_course(hub: SystemHub, foo: str, bar: str = "b", my_dependency=Depends(my_dep)):
        hub.plugins[Navigator].set_course_from_course_generator()
        print(foo, bar)
        return hub.plugins[Navigator].course
    ```

    """
    func_sig = inspect.signature(func)
    params = list(func_sig.parameters.values())
    params.remove(params[0])  # remove hub arg
    params.append(inspect.Parameter('queue_system_task',
                                    default=Depends(dependencies.queue_system_task_dependency),
                                    kind=inspect.Parameter.KEYWORD_ONLY))
    new_sig = func_sig.replace(parameters=params)

    @makefun.wraps(func, new_sig=new_sig)
    async def endpoint(*args, queue_system_task=Depends(dependencies.queue_system_task_dependency),
                       data_subscription_schema: DataSubscriptionSchema = None,
                       **kwargs):
        if data_subscription_schema is not None:
            data_subscription = DataSubscription(func=func,
                                                 args=args,
                                                 kw_args=tuple(sorted(kwargs.items())),
                                                 period_length=data_subscription_schema.period_length)
            res = await queue_system_task(lambda hub: hub.data.add_data_subscription(data_subscription))
            if not isinstance(res, Exception):
                JSONResponse(hash(data_subscription))
            else:
                JSONResponse(res, status_code=500)
        res = await queue_system_task(func, *args, **kwargs)
        return JSONResponse(res.to_json() if isinstance(res, DataModelBase) else JSONEncoder().encode(res),
                            status_code=200 if not isinstance(res, Exception) else 500)

    endpoint.engine_func = func
    return endpoint
