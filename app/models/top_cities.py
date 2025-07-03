from .base import Base
from sqlalchemy.orm import Mapped


class TopCities(Base):
    __tablename__ = "top_cities"

    name: Mapped[str]
    requests: Mapped[int]
