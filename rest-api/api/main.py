from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .config import get_config
from api.db import db
from api.public import api as public_api
from api.utils.logger import logger

settings = get_config()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/",
)

app.include_router(public_api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(
    "FastAPI Mongo Async API has been launched for %s environment!",
    settings.ENVIRONMENT,
)

@app.on_event("startup")
async def startup():
    logger.info("db connection startup")
    await db.connect_to_database(path = settings.DB_URI, 
                                 dbname = settings.DB_NAME)

@app.on_event("shutdown")
async def shutdown():
    logger.info("db connection startup")
    await db.close_database_connection()


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8080, reload=True)