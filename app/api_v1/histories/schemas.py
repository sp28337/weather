from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HistorySchemaBase(BaseModel):
    city: str

    model_config = ConfigDict(from_attributes=True)


class HistoryCreateSchema(HistorySchemaBase):
    user_id: str


class HistorySchema(HistorySchemaBase):
    timestamp: datetime
