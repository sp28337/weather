from pydantic import BaseModel, ConfigDict


class CitySchemaBase(BaseModel):
    name: str
    requested: int

    model_config = ConfigDict(from_attributes=True)


class CityCreateSchema(CitySchemaBase):
    pass


class CityUpdateSchema(CityCreateSchema):
    pass


class CityUpdatePartialSchema(CityCreateSchema):
    name: str | None = None
    requested: int | None = None


class CitySchema(CitySchemaBase):
    id: int
