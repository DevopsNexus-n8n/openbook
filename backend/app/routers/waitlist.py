from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import WaitlistEntry
from ..schemas import WaitlistIn, WaitlistOut

router = APIRouter(prefix="/api/waitlist", tags=["waitlist"])


@router.post("", response_model=WaitlistOut)
def join_waitlist(payload: WaitlistIn, db: Session = Depends(get_db)):
    email = payload.email.lower()
    exists = db.scalar(select(WaitlistEntry).where(WaitlistEntry.email == email))
    if not exists:
        db.add(WaitlistEntry(email=email, business_type=payload.business_type))
        db.commit()
    # Same response either way, so the endpoint doesn't reveal who has signed up.
    return WaitlistOut()
