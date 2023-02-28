import json
import os
from typing import List
from bson.json_util import dumps
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from api.db.database_manager import DatabaseManager
from api.models.generic import Article
from api.utils.logger import logger
from api.config import get_config


class MongoManager(DatabaseManager):
    """
    This class extends DatabaseManager
    which have the abstract methods to be re-used here.
    """
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str, dbname: str):
        """Inherited from databasemanager, connect to mongo
        """
        logger.info("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client[dbname]

        logger.info(
            "Connected to MongoDB - in articles environment!"
        )

    async def close_database_connection(self):

        logger.info("Closing connection to MongoDB - articles env")
        self.client.close()
        logger.info("MongoDB connection closed - articles env")

    async def articles_get_all(self) -> List[Article]:
        """Inherited from databasemanager, asynchronous method
           to be used from /articles/views
           returns list of all articles.
        """
        articles_list = []
        articles = self.db.articles.find()

        async for article in articles:
            del article["_id"]
            articles_list.append(json.loads(dumps(article)))

        return articles_list

    async def articles_by_sentence(self, content_text: str) -> list[Article]:
        """Inherited from databasemanager, asynchronous method
           to be used from /articles/views
           returns list of all articles where there is a sentence that matches
           exactly the input sentence
        """
        articles_list = []
        content_text = '\"' + content_text + '\"'
        articles = self.db.articles.find({
            "$text": {"$search": content_text
                      }})

        async for article in articles:
            del article["_id"]
            articles_list.append(json.loads(dumps(article)))

        return articles_list

    async def articles_by_keywords(self, keywords: str) -> list[Article]:
        """Inherited from databasemanager, asynchronous method
           to be used from /articles/views
           returns list of all articles where there on keyword matching
        """
        articles_list = []
        articles = self.db.articles.find({"$text": {"$search": keywords}})

        async for article in articles:
            del article["_id"]
            articles_list.append(json.loads(dumps(article)))

        return articles_list