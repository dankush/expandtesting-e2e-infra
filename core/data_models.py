# core/data_models.py
from pydantic import BaseModel, EmailStr
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

#... other models