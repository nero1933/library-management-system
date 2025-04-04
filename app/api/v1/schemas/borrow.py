from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BorrowCreateSchema(BaseModel):
    user_id: int
    book_id: int


class BorrowResponseSchema(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: Optional[datetime]
