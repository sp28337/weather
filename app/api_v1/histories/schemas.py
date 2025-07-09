from pydantic import BaseModel, ConfigDict


class HistorySchemaBase(BaseModel):
    user_id: str
    city: str

    model_config = ConfigDict(from_attributes=True)


class HistoryCreateSchema(HistorySchemaBase):
    pass


class HistorySchema(HistorySchemaBase):
    id: int
