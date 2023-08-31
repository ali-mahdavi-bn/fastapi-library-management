from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from models.Model import Author




class GetUser(BaseModel):
    id: int


class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    role: str

    @field_validator('name', 'username')
    def validate_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValueError('Field length should be between 2 and 100 characters')
        return value

    @field_validator('email')
    def validate_email(cls, email: str) -> str:
        if '@example.com' in email:
            raise ValueError("Email addresses from example.com are not allowed")
        return email

    @field_validator('password')
    def validate_password(cls, value):
        if len(value) < 8 or len(value) > 100:
            raise ValueError('Password length should be between 8 and 100 characters')
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter")
        return value

    @field_validator('role')
    def validate_role(cls, role: str) -> str:
        valid_roles = ['admin', 'user']
        if role not in valid_roles:
            raise ValueError("Invalid role. Supported roles are 'admin' and 'user'")
        return role


class UserUpdate(BaseModel):
    name: str
    username: str
    email: EmailStr
    role: str

    @field_validator('name', 'username')
    def validate_length(cls, value: str) -> str:
        if len(value) < 2 or len(value) > 100:
            raise ValueError('Field length should be between 2 and 100 characters')
        return value

    @field_validator('email')
    def validate_email(cls, email: str) -> str:
        if '@example.com' in email:
            raise ValueError("Email addresses from example.com are not allowed")
        return email

    @field_validator('role')
    def validate_role(cls, role: str) -> str:
        valid_roles = ['admin', 'user']
        if role not in valid_roles:
            raise ValueError("Invalid role. Supported roles are 'admin' and 'user'")
        return role


class UserOut(UserUpdate):
    id: int
    name: str
    username: str

    class Config:
        from_attributes = True

