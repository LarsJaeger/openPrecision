from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.persistence_model_base import PersistenceModelBase

if TYPE_CHECKING:
    from open_precision.core.model.action_response import ActionResponse

class Action(DataModelBase, PersistenceModelBase):
    __tablename__ = "Actions"

    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    initiator: Mapped[str] = mapped_column(init=True, default=None)
    function_identifier: Mapped[str] = mapped_column(init=True,
                                                     default=None)  # consists of the name of the class and the name of the function separated by a dot
    args: Mapped[list] = mapped_column(init=True, default=None, nullable=True, default_factory=list)
    kwargs: Mapped[dict] = mapped_column(init=True, default=None, nullable=True, default_factory=dict)
    action_response_id: Mapped[ActionResponse] = relationship(back_populates="action")