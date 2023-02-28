import pymongo
import scrapy
import logging

logger = logging.getLogger(__name__)


class MongoPipeline(object):
    """This is an item pipline
        after an item has been scraped and processed by a spider,
        it is sent to the pipline, in this case MongoPipline
        will add to a collection
    """
    collection_name = 'articles'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler) -> scrapy.Spider:
        """Create an instance from a crawler,
           returns and instance with mongo settings
           added as objects.
        """
        return cls(
            mongo_uri=crawler.settings.get('DB_URL'),
            mongo_db=crawler.settings.get('DB_NAME')
        )

    def open_spider(self, spider) -> None:
        """When the spider process starts
           this will initialse a connector intance
        """
        logger.info('Connecting to mongodb from mongo pipline.')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider) -> None:
        """When the spider process ends
           this will close the connection
        """
        logger.info('Closing connection from mongo pipline.')
        self.client.close()

    def process_item(self, item, spider) -> scrapy.Item:
        """Will be called by the process
           to insert a record in mongo
        """
        logger.info(f"Inserting to {self.collection_name}")
        self.db[self.collection_name].insert_one(dict(item))
        return item