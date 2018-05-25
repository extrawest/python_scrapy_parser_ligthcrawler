# -*- coding: utf-8 -*-

import pandas as pd
from LightCrawler.scripts.file_manager import FileManager
from LightCrawler.items import PricesItem, FoodSafetyItem


class LightCrawlerPipeline(object):

    def open_spider(self, spider):
        """
        Create DataFrame object when spider is opened
        """
        if spider.name == 'bancor_prices':
            fieldnames = list(PricesItem.fields.keys())
        else:
            fieldnames = list(FoodSafetyItem.fields.keys())
        fieldnames.sort()
        self.df = pd.DataFrame(columns=fieldnames)

    def close_spider(self, spider):
        """
        Save scraped data to 'csv' and 'xlsx' file when spider close
        """
        if spider.name == 'bancor_prices':
            columns = [
                'code',
                'name',
                'price_USD',
                'change24h',
                'liquidityDepth_USD',
                'volume24h_USD'
            ]
        else:
            columns = [
                'facility',
                'food_sector',
                'rating',
                'expiration_date',
                'address'
            ]
        self.df.fillna('', inplace=True)
        self.df.to_csv(
            FileManager(name=spider.name).file('csv'),
            columns=columns,
            index=False
        )
        writer = pd.ExcelWriter(FileManager(name=spider.name).file('xlsx'))
        self.df.to_excel(
            writer,
            sheet_name=spider.name,
            index=False,
            columns=columns
        )
        writer.save()

    def process_item(self, item, spider):
        """
        Fill DataFrame when process item
        """
        self.df = pd.concat([self.df, pd.DataFrame(dict(item), index=[0])])
        return item