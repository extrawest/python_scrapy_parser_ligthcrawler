# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BOT_NAME = 'LightCrawler'

SPIDER_MODULES = ['LightCrawler.spiders']

NEWSPIDER_MODULE = 'LightCrawler.spiders'

LOG_LEVEL = 'INFO'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 16

CONCURRENT_REQUESTS_PER_DOMAIN = 16

CONCURRENT_REQUESTS_PER_IP = 16

COOKIES_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

ITEM_PIPELINES = {
   'LightCrawler.pipelines.LightCrawlerPipeline': 300,
}
