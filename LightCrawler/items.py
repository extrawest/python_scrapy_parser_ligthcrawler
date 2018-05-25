# -*- coding: utf-8 -*-
import scrapy


class PricesItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    price_USD = scrapy.Field()
    volume24h_USD = scrapy.Field()
    liquidityDepth_USD = scrapy.Field()
    change24h = scrapy.Field()


class FoodSafetyItem(scrapy.Item):
    facility = scrapy.Field()
    food_sector = scrapy.Field()
    rating = scrapy.Field()
    expiration_date = scrapy.Field()
    address = scrapy.Field()
