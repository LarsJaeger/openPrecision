from __future__ import annotations

import inspect
from typing import Callable, Any, TYPE_CHECKING

import makefun
from fastapi import Depends
from starlette.responses import JSONResponse

from open_precision.api import dependencies as dependencies
from open_precision.core.model import DataModelBase, CustomJSONEncoder
from open_precision.core.model.data_subscription import DataSubscription

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


def _create_add_subscr(subscription_socket_id, data_subscription):
    def _add_subscr(hub: SystemHub):
        hub.data.add_data_subscription(subscription_socket_id, data_subscription)

    return _add_subscr


def engine_endpoint(func: Callable[[SystemHub, ...], Any]) -> Callable[[...], Any]:
    """
    Decorator to make fastapi endpoint functions from functions that need to be run in the engine (update loop in the
    main thread).

    The decorated function must have a variable of type SystemHub as their first positional argument.
    The following arguments can be treated as if the function was a FastAPI endpoint function, however it must still be
    decorated as such!
    The Endpoint will return the value returned by the decorated function as JSON (Attention: if it is a string, it will
    not be JSONEncoded to allow for custom Encoders to be used within the wrapped function!). The status code of the
    returned JSON will either be 200 (default), or 500 (if an error occured while executing the function).

    Usage:
    ```python
    @app.post("/generate{foo}")
    @engine_endpoint
    def _generate_course(hub: SystemHub, foo: str, bar: str = "b", my_dependency=Depends(my_dep)):
        hub.plugins[Navigator].set_course_from_course_generator()
        print(foo, bar)
        return hub.plugins[Navigator].course

    Engine endpoint requests  can also be subscribed to. This means that the endpoint will be called periodically and
    the returned value will be sent to the client via socketio. To subscribe to an endpoint, the client must send the
    request that should be subscribed to with the following query parameters:
    - subscription_socket_id: the socket id of the client that should be subscribed to the endpoint
    - subscription_period_length: the period length in milliseconds
    The endpoint will then return the hash of the subscription object. This hash will be the event_id that the data will
    be emitted with. The data will be emitted as a JSON string.
    ```

    """
    # TODO document schemes
    func_sig = inspect.signature(func)
    params = list(func_sig.parameters.values())
    params.remove(params[0])  # remove hub arg
    params.append(inspect.Parameter('queue_system_task',
                                    default=Depends(dependencies.queue_system_task_dependency),
                                    kind=inspect.Parameter.KEYWORD_ONLY))
    params.append(inspect.Parameter('subscription_socket_id',
                                    default=None,
                                    annotation=str | None,
                                    kind=inspect.Parameter.KEYWORD_ONLY))
    params.append(inspect.Parameter('subscription_period_length',
                                    default=None,
                                    annotation=int | None,
                                    kind=inspect.Parameter.KEYWORD_ONLY))
    new_sig = func_sig.replace(parameters=params)

    @makefun.wraps(func, new_sig=new_sig)
    async def endpoint(*args,
                       queue_system_task=Depends(dependencies.queue_system_task_dependency),
                       subscription_socket_id: str | None = None,
                       subscription_period_length: int | None = None,
                       **kwargs):
        # check for subscription
        if subscription_socket_id is not None and subscription_period_length is not None:
            # subscription requested

            data_subscription = DataSubscription(func=func,
                                                 args=args,
                                                 kw_args=tuple(sorted(kwargs.items())),
                                                 period_length=subscription_period_length)
            res = await queue_system_task(_create_add_subscr(subscription_socket_id, data_subscription))
            if isinstance(res, tuple) and isinstance(res[0], Exception):
                return JSONResponse(str(res[1]), status_code=500)
            else:
                return JSONResponse(str(hash(data_subscription)), status_code=200)

        else:
            # no subscription
            res = await queue_system_task(func, *args, **kwargs)
            if isinstance(res, tuple) and isinstance(res[0], Exception):
                return JSONResponse(str(res[1]), status_code=500)
            else:
                if isinstance(res, DataModelBase):
                    res = res.to_json()
                elif isinstance(res, str):
                    pass
                else:
                    res = CustomJSONEncoder().encode(res)

                print("res", res)
                print("type", type(res))
                return JSONResponse(res,
                                    status_code=200)

    return endpoint