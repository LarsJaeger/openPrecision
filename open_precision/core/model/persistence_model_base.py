from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column


class PersistenceModelBase:
    """
    This is the base class for the persistence model. Every class that inherits from this class will be mapped and
    can therefore be persisted in the database.
    """

    last_updated: Mapped[datetime] = mapped_column(init=True, default=None)
    last_updated_by: Mapped[str] = mapped_column(init=True, default=None)

    """
    To provide attributes stored in json (or if you want to define property based getter and setter methods for a mapped
    column for any other reason), the variable name of the mapped column must begin with an underscore. Additionally
    you must define a variable without the underscore that is not mapped, but instead contains a dataclass.field(...),
    otherwise the getters and setters cannot be defined. To provide attributes stored in json, this has to be done too.
    """