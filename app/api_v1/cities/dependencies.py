from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper, City
from . import crud


async def get_city_by_id(
    city_id: Annotated[int, Path()],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> City:
    city = await crud.get_city(session=session, city_id=city_id)
    if city is not None:
        return city

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"City {city_id} not found!",
    )
