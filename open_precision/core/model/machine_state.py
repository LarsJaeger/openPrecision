from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.persistence_model_base import PersistenceModelBase
if TYPE_CHECKING:
    from open_precision.core.model.position import Position


class MachineState(DataModelBase, PersistenceModelBase):

    __tablename__ = "MachineStates"

    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    steering_angle: Mapped[float] = mapped_column(init=True, default=None, nullable=True)  # in degrees, positive
    # means to the right
    speed: Mapped[float] = mapped_column(init=True, default=None, nullable=True)  # in m/s, negative values mean
    # reverse
    position: Position | None = field(init=True, default=None)
    _position: Mapped[str] = relationship(init=True, default=None, nullable=True, uselist=False, repr=False, back_populates="machine_state")  # in JSON format

    # TODO add fields for things like section control, implement state, etc.