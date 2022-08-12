from sqlalchemy.orm import mapped_column, Mapped

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.persistence_model_base import PersistenceModelBase


class MachineState(DataModelBase, PersistenceModelBase):

    __tablename__ = "MachineStates"

    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    steering_angle: Mapped[float] = mapped_column(default=None)  # in degrees, positive
    # means to the right
    speed: Mapped[float] = mapped_column(default=None)  # in m/s, negative values mean
    # reverse
    # TODO add fields for things like section control, etc.