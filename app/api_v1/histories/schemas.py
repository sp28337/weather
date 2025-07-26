from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HistorySchemaBase(BaseModel):
    city: str = Field(min_length=2, max_length=64)

    model_config = ConfigDict(from_attributes=True)

    @field_validator("city")
    @classmethod
    def city_must_not_be_blank_or_spaces(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("City cannot be blank or only spaces")
        return value


class HistoryCreateSchema(HistorySchemaBase):
    user_id: str


class HistoryCreateSchemaTest(HistoryCreateSchema):
    model_config = ConfigDict(extra="forbid", strict=True)


class HistorySchema(HistorySchemaBase):
    timestamp: datetime


class HistorySchemaTest(HistorySchema, HistoryCreateSchema):
    pass
