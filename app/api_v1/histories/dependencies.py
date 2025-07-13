from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure import get_session
from app.models import History
from . import crud


async def get_last_history(
    user_id: Annotated[str, Path()],
    session: AsyncSession = Depends(get_session),
) -> History:
    history = await crud.get_last_history(session=session, user_id=user_id)
    if history is not None:
        return history

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Hystory of user id: {user_id} not found!",
    )


async def get_user_histories(
    user_id: Annotated[str, Path()],
    session: AsyncSession = Depends(get_session),
) -> list[History]:
    histories = await crud.get_user_histories(session=session, user_id=user_id)
    if histories is not None:
        return histories

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Histories of user id: {user_id} not found!",
    )
