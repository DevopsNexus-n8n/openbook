from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class WaitlistIn(BaseModel):
    email: EmailStr
    business_type: str | None = None


class WaitlistOut(BaseModel):
    ok: bool = True


class SignupIn(BaseModel):
    business_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(max_length=128)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TenantOut(BaseModel):
    id: int
    name: str
    slug: str
    plan: str
    trial_ends_at: datetime | None


class MeOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    tenant: TenantOut
