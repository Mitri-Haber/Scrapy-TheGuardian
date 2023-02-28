from scrapy import signals
from scrapy.exceptions import IgnoreRequest
import pymongo
import logging

logger = logging.getLogger(__name__)


class TheguardianscrapperSpiderMiddleware(object):
    """hooks in Scrapy's request/response processing
       in order to add custom functionality for responses
       that are sent to the spiders.
    """

    @classmethod
    def from_crawler(cls, crawler):
        """This method is used by Scrapy to create the spiders.
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TheguardianscrapperDownloaderMiddleware:
    """hooks in Scrapy's request/response processing
       in order to alter global requests and responses.
    """

    def __init__(self, mongo_uri, mongo_db) -> None:

        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection = 'articles'

    @classmethod
    def from_crawler(cls, crawler):
        """In the middleware, it
           will be used by Scrapy to instantiate a spider process
           In this case we provide it with mongo settings.
           in order to be used in the process_request
        """
        s = cls(
                mongo_uri=crawler.settings.get('DB_URL'),
                mongo_db=crawler.settings.get('DB_NAME')
            )
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider) -> None:
        """ Called for all request that goes through the downloader
            middleware.
            In this case It's used here to check if article was already
            scraped by searching in the collection.
            If it's found the request will not go through.
        """

        article_url = request.url
        cursor = self.db[self.collection].find_one({"url": article_url})
        if cursor:
            logger.info(f'Ignoring {article_url}, already exists')
            raise IgnoreRequest
        return None

    def process_response(self, request, response, spider) -> None:
        """To process responses globally.
        """
        return response

    def process_exception(self, request, exception, spider) ->None:
        """Can be used to catch and process exeptions
        """
        pass

    def spider_opened(self, spider) -> None:

        spider.logger.info("Opened mongo connection from DownloaderMiddleware")
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def spider_closed(self, spider) -> None:
        """ Closes the DB connection when the spider is closed.
        """
        spider.logger.info("Closed mongo connection from DownloaderMiddleware")
        self.client.close()