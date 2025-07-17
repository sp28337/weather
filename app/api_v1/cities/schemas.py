from pydantic import BaseModel, ConfigDict


class CitySchemaBase(BaseModel):
    name: str
    requested: int

    model_config = ConfigDict(from_attributes=True)


class CityCreateSchema(CitySchemaBase):
    pass


class CityUpdateSchema(CitySchemaBase):
    pass


class CitySchema(CitySchemaBase):
    id: int
