from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from open_precision.core.model.action import Action
from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.persistence_model_base import PersistenceModelBase


class ActionResponse(DataModelBase, PersistenceModelBase):
    __tablename__ = "ActionResponses"

    id: Mapped[int] = mapped_column(init=True, primary_key=True, default=None)

    action_id: Mapped[int] = mapped_column(ForeignKey("Actions.id"), init=True, repr=False, default=None, nullable=True)
    action: Mapped[Action] = relationship(init=True, default=None, back_populates='action_response')

    success: Mapped[bool] = mapped_column(init=True, default=None, nullable=True)

    response: Mapped[str] = mapped_column(init=True, default=None, nullable=True)  # json of either the return value or the exception