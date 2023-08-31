from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from utility.CustomValidations import CustomValidations


class BookCreate(BaseModel):
    title: str
    descriptions: str
    author_id: int
    genre_id: int
    publication_date: datetime
    isbn: str
    price: int
    is_active: bool
    soft_delete: bool
    created_at: datetime
    updated_at: datetime

    @field_validator('author_id')
    def validate_length(cls, value):
        if CustomValidations.validate_int(value):
            raise ValueError('Field be must be an integer')
        return value

    @field_validator('title')
    def validate_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValueError('Field length should be between 2 and 100 characters')
        return value


class BookUpdate(BaseModel):
    title: str
    author_id: int
    publication_date: datetime
    isbn: str
    price: int
    is_active: bool
    soft_delete: bool
    created_at: datetime
    updated_at: datetime

    @field_validator('author_id')
    def validate_length(cls, value):
        if CustomValidations.validate_int(value):
            raise ValueError('Field be must be an integer')
        return value

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
