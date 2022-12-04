from __future__ import annotations

from typing import Any, Callable


def validate_value(value: Any, rule: Callable[[Any], bool], rule_description: str | None = None) -> bool:
    """
    Checks if value is valid according to rule.

    :param value: value to check
    :param rule: function that returns True if value is valid
    :param rule_description: description of rule for error message

    :return: True if value is valid according to rule, raises ValueError otherwise

    :raises ValueError: if value is not valid according to rule
    """
    if rule_description is None and rule.__doc__ is not None:
        rule_description = "Rule generated from rule docstring: " + rule.__doc__
    if not rule(value):
        raise ValueError(value, rule_description)
    return True
