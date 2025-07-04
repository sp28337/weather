from .base import Base
from sqlalchemy.orm import Mapped


class City(Base):

    name: Mapped[str]
    requested: Mapped[int]
