import os

BOT_NAME = 'TheguardianScrapper'
SPIDER_MODULES = ['TheguardianScrapper.spiders']
NEWSPIDER_MODULE = 'TheguardianScrapper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Logger settings
LOG_FILE = 'crawler.log'
LOG_LEVEL = 'INFO'

# Enable or disable spider middlewares and set priority
SPIDER_MIDDLEWARES = {
    'TheguardianScrapper.middlewares.TheguardianscrapperSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares and set priority
DOWNLOADER_MIDDLEWARES = {
   'TheguardianScrapper.middlewares.TheguardianscrapperDownloaderMiddleware': 543,
}

# Enable or disable item pipline and set priority
ITEM_PIPELINES = {
    'TheguardianScrapper.pipelines.MongoPipeline': 300,
}

# Mongo config
DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")

# Cache previous urls, can be used to not re-process previous urls.
HTTPCACHE_ENABLED = False
HTTPCACHE_DIR = 'httpcache'

