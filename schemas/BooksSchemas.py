from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class BookCreate(BaseModel):
    title: str
    author_id: int
    is_active: bool

    @field_validator('title')
    def validate_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValueError('Field length should be between 2 and 100 characters')
        return value


class BookOut(BaseModel):
    title: str
    author_id: int

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title: str
    author_id: int
    is_active: Optional[bool]
    soft_delete: Optional[bool]

    @field_validator('title')
    def validate_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValueError('Field length should be between 2 and 100 characters')
        return value