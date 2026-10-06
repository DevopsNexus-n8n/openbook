import re
import secrets
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..deps import get_current_user
from ..models import Tenant, User, utcnow
from ..schemas import LoginIn, MeOut, SignupIn, TenantOut, TokenOut
from ..security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api", tags=["auth"])

# Verified against when the email doesn't exist, so login takes the same time either way.
_DUMMY_HASH = hash_password("not-a-real-password")


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return (slug or "business")[:48]


def _unique_slug(db: Session, name: str) -> str:
    base = _slugify(name)
    slug = base
    while db.scalar(select(Tenant.id).where(Tenant.slug == slug)):
        slug = f"{base}-{secrets.token_hex(2)}"
    return slug


@router.post("/auth/signup", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupIn, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if db.scalar(select(User.id).where(User.email == email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")
    tenant = Tenant(
        name=payload.business_name.strip(),
        slug=_unique_slug(db, payload.business_name),
        plan="trial",
        trial_ends_at=utcnow() + timedelta(days=settings.trial_days),
    )
    user = User(tenant=tenant, email=email, password_hash=hash_password(payload.password), role="owner")
    db.add_all([tenant, user])
    db.commit()
    return TokenOut(access_token=create_access_token(user.id, tenant.id))


@router.post("/auth/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    ok = verify_password(payload.password, user.password_hash if user else _DUMMY_HASH)
    if not user or not ok or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email or password is incorrect")
    return TokenOut(access_token=create_access_token(user.id, user.tenant_id))


@router.get("/me", response_model=MeOut)
def me(user: User = Depends(get_current_user)):
    t = user.tenant
    return MeOut(
        id=user.id,
        email=user.email,
        role=user.role,
        tenant=TenantOut(id=t.id, name=t.name, slug=t.slug, plan=t.plan, trial_ends_at=t.trial_ends_at),
    )
