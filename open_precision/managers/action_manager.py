from __future__ import annotations
from typing import TYPE_CHECKING

import json
import redis

from open_precision.core.model.action import Action
from open_precision.core.model.action_response import ActionResponse

if TYPE_CHECKING:
    from open_precision.manager import Manager


class ActionManager:

    @staticmethod
    def enable_action(func):
        func.action_enabled = True
        return func

    @staticmethod
    def check_action_enabled(func):
        return hasattr(func, 'action_enabled')

    def __init__(self, manager: Manager):
        self._manager = manager
        self._redis = redis.Redis(host='redis', port=6379, db=1)

    def queue_action(self, action: Action):
        match action:
            case Action():
                self._redis.rpush('action', action.to_json())
            case str():
                self._redis.rpush('action', action)

            case _:
                raise TypeError(f"Action must be of type Action or str (json), not {type(action)}")

    def _get_action(self):
        json_action = self._redis.lpop('action')
        print(json_action)
        action = Action(**json.loads(json_action)) if json_action is not None else None
        return action

    def handle_action(self, action: Action):
        function_identifier_decomposed = action.function_identifier.split('.')
        obj = self._manager
        len_of_function_identifier_decompose = len(
            function_identifier_decomposed)  # save, so it doesn't have to be calculated every iteration
        if function_identifier_decomposed[0] == 'plugins' and len_of_function_identifier_decompose > 1:
            obj = self._manager.plugins[self._manager.plugin_name_mapping[function_identifier_decomposed[1]]]
        for index, identifier in enumerate(function_identifier_decomposed):
            try:
                obj = getattr(obj, identifier)
            except AttributeError:
                raise AttributeError(f"Object {obj} has no attribute {identifier}")
            if index == len_of_function_identifier_decompose - 1:
                # last iteration, so this item must be a function that is enabled as an action
                if callable(obj) and ActionManager.check_action_enabled(obj):
                    # execute function
                    success = None
                    try:
                        return_value = obj(*action.args, **action.kw_args)
                        success = True
                    except Exception as e:
                        return_value = e
                        success = False
                    return ActionResponse(action_id=action.id, response=return_value, success=success)
                else:
                    raise AttributeError(f"Object {obj} is not callable or not enabled as an action")

    def handle_actions(self, amount: int = 10) -> list[ActionResponse]:
        """Executes the passed amount of actions and returns a list of ActionResponses that should be delivered to the
        initiator of the action."""
        action_responses = []
        for _ in range(amount):
            action = self._get_action()
            if action is None:
                return []
            action_response = self.handle_action(action)
            action_responses.append(action_response)
        return action_responses
