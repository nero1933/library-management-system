from datetime import date

from pydantic import BaseModel, validator, field_validator, ConfigDict


class PublisherSchema(BaseModel):
    name: str
    established_year: int

    @field_validator('established_year')
    def validator_established_year(cls, value):
        if value > date.today().year:
            raise ValueError("Year of establishment cannot be in the future")
        if value < 1700:
            raise ValueError("Year of establishment cannot before 1700")

        return value

class PublisherResponseSchema(BaseModel):
    id: int
    name: str
    established_year: int

    model_config = ConfigDict(from_attributes=True)
