import scrapy
from TheguardianScrapper.items import ArticleItem
import json
from .process_helper import process


class TheguardianSpider(scrapy.Spider):
    """enherits from scrapy.Spider, and loads filter config filter_config.json
       it will scrape the guardian news page at a depth 3
       starting from the home pageS
    """
    name = "theguardian"
    allowed_domains = ['www.theguardian.com']

    def __init__(self):

        self.config = json.load(open('filter_config.json'))

        self.start_urls = self.config['start']['start_urls']
        self.pages_from_menu_filter = self.config['parse']['pages_from_menu_filter']
        self.article_url_selector = self.config['parse_page']['article_url_selector']
        self.next_page_selector = self.config['parse_page']['next_page_selector']
        self.content_text_selector = self.config['parse_article']['content_text_selector']
        self.author_selector = self.config['parse_article']['author_selector']
        self.content_text_selector = self.config['parse_article']['content_text_selector']
        self.author_selector = self.config['parse_article']['author_selector']
        self.processor = process()

        super(TheguardianSpider, self).__init__()

    def parse(self, response) -> scrapy.Request:
        """started by the process, it will take the starting page as input
           ("https://www.theguardian.com/international") and will return urls
           from the menu for other category pages.
        """
        PAGES_FROM_MENU_FILTER = self.pages_from_menu_filter
        for news_url in response.xpath(PAGES_FROM_MENU_FILTER).extract():
            self.logger.info(f'Foud menu url at depth 1:{response.url}')
            yield scrapy.Request(
                    url=news_url,
                    callback=self.parse_articles_page
            )

    def parse_articles_page(self, response) -> scrapy.Request:
        """Called by the function parse, it will scrape each category page
           it will find article links and paginators using xpath queries
           the links retuned by xpath queries for articles will be passed.
           to parse_article.
           the links returned by queries for paginators urls
           will be passed again to this method in order to find article urls
        """
        ARTICLE_URL_SELECTOR = self.article_url_selector
        for article_url in response.xpath(ARTICLE_URL_SELECTOR).extract():
            self.logger.info(f'Foud article url at depth 2:{response.url}')
            yield scrapy.Request(
                    url=article_url,
                    callback=self.parse_article
            )

        NEXT_PAGE_SELECTOR = self.next_page_selector
        next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()
        if(next_page):
            yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse_articles_page
                    )

    def parse_article(self, response) -> ArticleItem:
        """Called by parse_articles_page to scrape and process an article page
           Uses two processing functions proc_url and proc_content intialised
           as methods for this class, imported from procec_helper.Returns
           a dict containing article content,url,label,
           published_at,headline,author
        """
        self.logger.info(f'Processing at depth 3 :{response.url}')
        processed_url = self.processor.proc_url(response.request.url)
        processed_content = self.processor.proc_content(response)

        item = ArticleItem()
        item['content'] = processed_content['content']
        item['url'] = processed_url['url']
        item['label'] = processed_url['label']
        item['published_at'] = processed_url['published_at']
        item['headline'] = processed_url['headline']
        item['author'] = processed_content['author']

        yield item