from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column


class PersistenceModelBase:
    """This is the base class for the persistence model."""
    last_updated: Mapped[datetime] = mapped_column(init=False, default=None)
    last_updated_by: Mapped[str] = mapped_column(init=False, default=None)