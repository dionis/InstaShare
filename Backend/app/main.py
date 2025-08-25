from fastapi import FastAPI
from app.core.config import Settings

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)


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
