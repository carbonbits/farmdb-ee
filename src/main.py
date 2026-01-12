from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from core.storage.database import DB
from settings import settings
from apps.api.utilities import api_tags_metadata

@asynccontextmanager
async def lifespan(app: FastAPI):
    DB.connect()
    yield

    DB.disconnect()

application = FastAPI(
    title="farmdb",
    description="Profesional farm management tooling",
    terms_of_service="https://agin.africa/farmdb/terms/",
    version=settings.version,
    lifespan=lifespan,
    openapi_tags=api_tags_metadata,
)


if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=5700)
