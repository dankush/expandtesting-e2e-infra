# core/data_models.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserRegisterResponse(BaseModel): # Update based on the JSON response
    success: bool
    status: int
    message: str
    data: dict

class NoteCreateRequest(BaseModel):
    title: str
    description: str
    category: str # Literal["Home", "Work", "Personal"] # Requires Python 3.8+

class NoteResponse(BaseModel): # Represent a single Note
    id: str
    title: str
    description: str
    category: str
    completed: bool
    created_at: str
    updated_at: str
    user_id: str

class UserRegistrationRequest(BaseModel):
    """Request model for user registration."""
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value

class UserRegistrationResponse(BaseModel):
    """Response model for user registration."""
    success: bool
    status: int
    message: str
    data: dict

#... other models