from typing import Optional

from pydantic import BaseModel, field_validator


class AuthorCreate(BaseModel):
    name: str
    user_id: int

    @field_validator('name')
    def validate_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValueError('Field length should be between 2 and 100 characters')
        return value


class AuthorOut(BaseModel):
    id: int
    name: str
    user_id: int

    class Config:
        from_attributes = True


class AuthorUpdate(BaseModel):
    name: str
    user_id: int
    is_active: Optional[bool]
    soft_delete: Optional[bool]

    @field_validator('name')
    def validate_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValueError('Field length should be between 2 and 100 characters')
        return value
