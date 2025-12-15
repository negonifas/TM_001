from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID
    nickname: str
    created_at: datetime
    last_seen: datetime

    class Config:
        from_attributes = True


class AuthRequest(BaseModel):
    nickname: str = Field(..., min_length=1)
    create_if_missing: bool = False


class LoginRequest(BaseModel):
    login: str
    password: str


class AuthResponse(BaseModel):
    user: User
    csrf_token: str


class ProjectBase(BaseModel):
    name_ru: str = Field(..., min_length=1, description="Project title (ru)")
    name_en: Optional[str] = Field(default="")
    organization_ru: Optional[str] = Field(default="")
    organization_en: Optional[str] = Field(default="")
    direction: Optional[str] = Field(default="")
    scope: Optional[str] = Field(default="")
    focus: Optional[str] = Field(default="")
    profile_type: Optional[str] = Field(default="")
    specialization: Optional[str] = Field(default="")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    organization_ru: Optional[str] = None
    organization_en: Optional[str] = None
    direction: Optional[str] = None
    scope: Optional[str] = None
    focus: Optional[str] = None
    profile_type: Optional[str] = None
    specialization: Optional[str] = None


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
