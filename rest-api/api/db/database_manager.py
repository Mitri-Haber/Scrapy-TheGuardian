from abc import abstractmethod
from typing import List
from api.models.generic import Article


class DatabaseManager:
    """
    This class is meant to be extended from
    ./mongo_manager.py which will be the actual connection to mongodb.
    """

    @property
    def client(self):
        raise NotImplementedError
    
    @property
    def db(self):
        raise NotImplementedError
    
    @abstractmethod
    async def connect_to_database(self, path: str):
        """ connect_to_database will be overriden
            in mongomanager
        """
        pass
    
    @abstractmethod
    async def close_database_connection(self):
        """ close_database_connection will be overriden
            in mongomanager
        """
        pass

    @abstractmethod
    async def articles_get_all(self) -> List[Article]:
        """ Method to be used from api endpoints will be overriden
            in mongomanager
        """
        pass

    @abstractmethod
    async def articles_by_sentence(self, content_text: str) -> List[Article]:
        """ Method to be used from api endpoints will be overriden
            in mongomanager
        """
        pass

    @abstractmethod
    async def articles_by_keywords(self, keywords: str) -> List[Article]:
        """ Method to be used from api endpoints will be overriden
            in mongomanager
        """
        pass