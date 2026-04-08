from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.monitors import router as monitors_router
from app.db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Create tables if not using Alembic currently
Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(monitors_router, prefix=f"{settings.API_V1_STR}/monitors", tags=["monitors"])

@app.get("/")
@limiter.limit("10/minute")
def read_root(request: Request):
    return {"message": f"Welcome to the {settings.PROJECT_NAME}"}
