from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class CitySchemaBase(BaseModel):
    name: str = Field(min_length=2, max_length=64)
    requested: int = Field(ge=1)

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank_or_spaces(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name cannot be blank or only spaces")
        return value


class CityCreateSchema(CitySchemaBase):
    pass


class CityUpdateSchema(CitySchemaBase):
    pass


class CitySchema(CitySchemaBase):
    id: int
