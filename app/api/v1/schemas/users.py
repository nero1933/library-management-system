from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     from_attributes = True


class UserAuthSchema(BaseModel):
    email: str
    password: str

    # class Config:
    #     from_attributes = True


class TokenDataSchema(BaseModel):
    access_token: str
