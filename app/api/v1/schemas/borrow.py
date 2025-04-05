from datetime import datetime
from typing import Optional, Set

from pydantic import BaseModel, validator, field_validator, ConfigDict


class BorrowCreateSchema(BaseModel):
    user_id: int
    book_id: int

class BorrowMultipleCreateSchema(BaseModel):
    book_ids: Set[int]

    @field_validator('book_ids')
    def check_not_empty(cls, value):
        if not value:
            raise ValueError('book_ids cannot be empty')

        return value

class BorrowResponseSchema(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
