from datetime import datetime, UTC

from .base import Base

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class History(Base):
    user_id: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC),
        server_default=func.now(),
    )
