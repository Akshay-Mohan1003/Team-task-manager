from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models import RoleEnum, StatusEnum

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.MEMBER

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    role: RoleEnum
    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TaskCreate(BaseModel):
    title: str
    project_id: str
    assignee_id: str
    due_date: Optional[str] = None
