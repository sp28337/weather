from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .profile import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    profile: Mapped["Profile"] = relationship(back_populates="user")
