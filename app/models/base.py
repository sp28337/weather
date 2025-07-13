from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
)
from app.actions import pluralize


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        return pluralize(self.__name__.lower())

    id: Mapped[int] = mapped_column(primary_key=True)
