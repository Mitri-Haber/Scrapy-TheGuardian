
from functools import lru_cache
from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    """app config settings
    """
    PROJECT_NAME: str = 'articles'
    VERSION: str = 'v1'
    DESCRIPTION: str = 'query articles'
    ENVIRONMENT: str = 'STG'
    DB_URI = os.getenv("DB_URL")
    DB_NAME = os.getenv("DB_NAME")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    COLLECTION_NAME= 'theguardian'

    class Config:
        case_sensitive = True

@lru_cache
def get_config():
    return Settings()
