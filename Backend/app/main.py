from fastapi import FastAPI, Depends
from app.core.config import Settings
from app.db.base import get_db, SessionLocal, Base, engine
from app.db.seed import create_initial_data

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        create_initial_data(db)
    finally:
        db.close()


@app.get("/", tags=["Health Check"])
async def read_root():
    return {"message": "Welcome to InstaShare Backend!"}


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "ok",
        "service_name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }
