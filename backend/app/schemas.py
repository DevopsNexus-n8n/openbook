from pydantic import BaseModel, EmailStr


class WaitlistIn(BaseModel):
    email: EmailStr
    business_type: str | None = None


class WaitlistOut(BaseModel):
    ok: bool = True
