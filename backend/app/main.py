from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models  # noqa: F401  (registers tables)
from .config import settings
from .db import Base, engine
from .routers import waitlist


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Stage 1 only. Stage 2 replaces this with Alembic migrations.
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Openbook API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}


app.include_router(waitlist.router)
