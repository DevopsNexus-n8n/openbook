import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .db import get_db
from .models import User
from .security import decode_token

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(status.HTTP_401_UNAUTHORIZED, "Sign in again", headers={"WWW-Authenticate": "Bearer"})
    if creds is None:
        raise unauthorized
    try:
        payload = decode_token(creds.credentials)
    except jwt.PyJWTError:
        raise unauthorized
    user = db.get(User, int(payload["sub"]))
    # The tenant in the token must match the user's real tenant. Never trust the token alone.
    if user is None or not user.is_active or user.tenant_id != payload.get("tid"):
        raise unauthorized
    return user


def current_tenant_id(user: User = Depends(get_current_user)) -> int:
    """Use this in every route that touches business data, and filter every query by it."""
    return user.tenant_id
