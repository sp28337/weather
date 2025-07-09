from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from models import db_helper
from . import crud
from .schemas import (
    HistoryCreateSchema,
    HistorySchema,
)


router = APIRouter(tags=["History"])


@router.post(
    "/",
    response_model=HistorySchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_history(
    new_history: HistoryCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_history(session=session, new_history=new_history)
