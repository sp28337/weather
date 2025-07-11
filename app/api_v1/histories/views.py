from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.infrastructure import get_session
from . import crud
from .dependencies import get_last_history, get_user_histories
from .schemas import (
    HistoryCreateSchema,
    HistorySchema,
)


router = APIRouter(tags=["History"])


@router.get("/user-histories/{user_id}/", response_model=list[HistorySchema])
async def get_user_histories(
    user_histories: list[HistorySchema] = Depends(get_user_histories),
):
    return user_histories


@router.get("/last-history/{user_id}/", response_model=HistorySchema)
async def get_last_history(
    last_hystory: HistorySchema = Depends(get_last_history),
):
    return last_hystory


@router.post(
    "/",
    response_model=HistorySchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_history(
    new_history: HistoryCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    return await crud.create_history(session=session, new_history=new_history)
