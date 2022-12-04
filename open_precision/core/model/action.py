from __future__ import annotations

import json
from dataclasses import field
from typing import TYPE_CHECKING, List, Any, Dict

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.persistence_model_base import PersistenceModelBase

if TYPE_CHECKING:
    from open_precision.core.model.action_response import ActionResponse


class Action(DataModelBase, PersistenceModelBase):
    __tablename__ = "Actions"

    id: Mapped[int] = mapped_column(init=True, primary_key=True, default=None)

    initiator: Mapped[str] = mapped_column(init=True, default=None, nullable=True)
    function_identifier: Mapped[str] = mapped_column(init=True,
                                                     default=None)  # consists of the name of the class and the name
    # of the function separated by a dot; if a plugin should be accessed the format is plugins.<plugin_class_name>

    args: List[Any] = field(init=True, default_factory=list)
    _args: Mapped[str] = mapped_column(init=True, default=None, repr=False, nullable=True)  # json of the arguments

    kw_args: Dict[str, Any] = field(init=True, default_factory=dict)
    _kw_args: Mapped[str] = mapped_column(init=True, default=None, repr=False, nullable=True) # json of the keyword arguments

    action_response: Mapped[ActionResponse] = relationship(init=True, default=None, repr=False, uselist=False, back_populates='action')

    @property
    def args(self) -> List[Any]:
        return json.loads(self._args) if self._args is not None else []

    @args.setter
    def args(self, args: List):
        self._args = json.dumps(args)

    @property
    def kw_args(self) -> Dict[Any, Any]:
        return json.loads(self._kw_args) if self._kw_args is not None else {}

    @kw_args.setter
    def kw_args(self, kw_args: Dict):
        self._args = json.dumps(kw_args)
