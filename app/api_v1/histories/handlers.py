from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from app.api_v1.histories.service import HistoryService
from app.core.exceptions import HistoryNotFoundException
from app.core.dependencies import get_history_service
from app.api_v1.histories.schemas import (
    HistorySchema,
)


router = APIRouter(prefix="/histories", tags=["History"])


@router.get("/user-histories/{user_id}/", response_model=list[HistorySchema])
async def get_user_histories(
    user_id: int,
    history_service: Annotated[HistoryService, Depends(get_history_service)],
):
    return await history_service.read_user_histories(user_id=user_id)


@router.get("/last-history/{user_id}/", response_model=HistorySchema | None)
async def get_last_history(
    user_id: str,
    history_service: Annotated[HistoryService, Depends(get_history_service)],
):
    try:
        return await history_service.read_last_history(user_id=user_id)
    except HistoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail,
        )
