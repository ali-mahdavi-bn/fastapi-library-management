from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BorrowingCreate(BaseModel):
    book_id: int
    user_id: int
    borrowed_at: datetime
    expertime_at: datetime


class BorrowingOut(BaseModel):
    book_id: int
    user_id: int
    borrowed_at: datetime
    expertime_at: datetime
    taken_back_at: datetime

    class Config:
        from_attributes = True


class BorrowingUpdate(BaseModel):
    book_id: Optional[int]
    user_id: Optional[int]
    borrowed_at: Optional[datetime]
    expertime_at: Optional[datetime]
    taken_back_at: Optional[datetime]
    is_active: Optional[bool]
    soft_delete: Optional[bool]


class BorrowingOutUpdate(BaseModel):
    book_id: Optional[int]
    user_id: Optional[int]
    borrowed_at: Optional[datetime]
    expertime_at: Optional[datetime]
    taken_back_at: Optional[datetime]
    is_active: Optional[bool]
    soft_delete: Optional[bool]
