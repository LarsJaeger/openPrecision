from sqlalchemy.orm import Mapped, mapped_column, relationship

from open_precision.core.model.action import Action
from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.persistence_model_base import PersistenceModelBase


class ActionResponse(DataModelBase, PersistenceModelBase):
    __tablename__ = "ActionResponses"

    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    action_id: Mapped[int] = mapped_column(init=True, default=None)
    action: Mapped[Action] = relationship("Action", back_populates="action_response")

    response: Mapped[str] = mapped_column(init=True, default=None)  # json of either the return value or the exception
    success: Mapped[bool] = mapped_column(init=True, default=None)
