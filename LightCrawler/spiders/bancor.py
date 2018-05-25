# -*- coding: utf-8 -*-

import json
import scrapy
from decimal import Decimal
from LightCrawler.items import PricesItem


class BancorPricesSpider(scrapy.Spider):
    """
    Spider for receiving criptocurency prices from
    site 'https://www.bancor.network'
    """
    name = "bancor_prices"
    allowed_domains = ["bancor.network"]
    prices_url = 'https://api.bancor.network/0.1/currencies/tokens'
    prices_query = '?limit=100&skip=0&fromCurrencyCode=ETH&includeTotal=false&orderBy=liquidityDepth&sortOrder=desc'
    currency_url = 'https://api.bancor.network/0.1/currencies/rate'
    currency_query = '?fromCurrencyCode=ETH&toCurrencyCodes=USD'
    USD = 0

    def start_requests(self):
        """
        Getting current exchange ETH/Dollar
        """
        yield scrapy.Request(self.currency_url + self.currency_query,
                             self.currency_price)

    def currency_price(self, response):
        """
        Method is in charge of processing the response and returning scraped
        prices data
        """
        data = json.loads(response.body_as_unicode())
        self.USD = data.get('data', {}).get('USD', 0)
        yield scrapy.Request(self.prices_url + self.prices_query, self.parse)

    def parse(self, response):
        """
        Method is in charge of processing the response and returning scraped
        prices data
        """
        price_item = PricesItem()
        data = json.loads(response.body_as_unicode())
        currencies = data.get('data', {}).get('currencies', {}).get('page', [])
        for currency in currencies:
            if 'code' in currency and 'price' in currency:
                price_item['code'] = currency['code']
                price_item['price_USD'] = currency['price'] * self.USD
                price_item['change24h'] = currency.get('change24h')
                price_item['volume24h_USD'] = self._volume24h_price(currency)
                price_item['liquidityDepth_USD'] = self._liquidity_deph_price(currency)
                price_item['name'] = currency['name']
                yield price_item

    def _volume24h_price(self, currency):
        """
        Converting raw data "volume24h" from ETH to Dollar
        """
        volume24h = int(currency.get('volume24h', '0'))
        if volume24h:
            return Decimal(int(currency.get('volume24h', '0'))) * \
               Decimal(self.USD) / 10 ** \
               currency.get('numDecimalDigits', 0)
        else:
            return 0

    def _liquidity_deph_price(self, currency):
        """
        Converting raw data "liquidityDepth" from ETH to Dollar
        """
        return float(currency.get('liquidityDepth', '0')) * self.USD