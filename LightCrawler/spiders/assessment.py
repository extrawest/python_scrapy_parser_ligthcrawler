# -*- coding: utf-8 -*-

import scrapy
import logging
from LightCrawler.items import FoodSafetyItem


class SuppliersAssessmentSpider80(scrapy.Spider):
    """
    Spider for SQFI audit type 'SQF Food Safety Audit Edition 8.0'
    """
    name = "suppliers_assessment_8_0"
    allowed_domains = [
        "sqfi.com",
        'parkcitygroup.com',
        'ac.parkcitygroup.com']
    search_url = 'https://www.sqfi.com/suppliers/assessment-database/public-search/'
    sqf_food = 'SQF Food Safety Audit Edition 8.0'
    filters = (
        "*//a[contains(., 'View SQFI Certified Suppliers')]/@href",
        "//a[contains(., 'Find')]/@onclick",
        "//table/tbody/tr",
        "//a[contains(., 'Next Page')]",
        "//div[contains(@class, 'table-pagination')]/div/text()",
        "//a[contains(., 'Next Page')]/@onclick",
        "//select[contains(., '{}')]/@name".format(sqf_food),
        "//option[contains(., '{}')]/@value".format(sqf_food),
        "//select[contains(., 'Seafood Processing')]/@name",
        "//select[contains(., 'Seafood Processing')]/option/@value",
        "//select[contains(., 'Fails to comply')]/@name",
        "//select[contains(., 'Fails to comply')]/option/@value",
        "//select[contains(., 'United States')]/@name",
        "//option[contains(., 'United States')]/@value",
    )

    def start_requests(self):
        """
        Get start page "Public Search" by "https://www.sqfi.com"
        """
        yield scrapy.Request(self.search_url, self.redirect_to)

    def redirect_to(self, response):
        """
        Redirect to filter form "View SQFI Certified Suppliers"
        """
        redirect_url = response.xpath(self.filters[0]).extract_first()
        yield scrapy.Request(redirect_url, self.first_submit)

    def first_submit(self, response):
        """
        Performing first click of find button with filled form data
        """
        find_action = response.xpath(self.filters[1]).extract_first()
        form_data = self._form_data(response)
        form_data.update(
            {'submitController': find_action.split(';')[1].split("'")[1]}
        )
        yield scrapy.FormRequest.from_response(
            response,
            formdata=form_data,
            callback=self.parse,
        )

    def parse(self, response):
        """
        Parsing all pages of search result
        """
        food_safety = FoodSafetyItem()
        table = response.xpath(self.filters[2]).extract()
        for row in table:
            row = scrapy.Selector(text=row).xpath('//td').extract()
            row = list(['\n'.join(scrapy.Selector(text=_).xpath('//td/text()').extract()).strip()
                        for _ in row][:-1])
            food_safety['facility'] = row[0]
            food_safety['food_sector'] = row[1]
            food_safety['rating'] = row[2]
            food_safety['expiration_date'] = row[3]
            food_safety['address'] = row[4]
            yield food_safety
        next_page = response.xpath(self.filters[3])
        info = response.xpath(self.filters[4]).extract_first()
        self.log('Page {} successfully processed '.format(info), level=logging.INFO)
        if next_page:
            next_action = next_page[0].xpath(self.filters[5]).extract_first()
            form_data = self._form_data(response)
            form_data.update({
                'submitController': next_action.split(';')[1].split("'")[1]
            })
            yield scrapy.FormRequest.from_response(
                response,
                formdata=form_data,
                callback=self.parse,
            )

    def _form_data(self, response):
        """
        Filling in search form
        """
        SQFI_audit_type = response.xpath(self.filters[6]).extract_first()
        SQFI_audit_type_val = response.xpath(self.filters[7]).extract_first()
        food_sector_categories = response.xpath(self.filters[8]).extract_first()
        food_sector_categories_val = response.xpath(self.filters[9]).extract()
        audit_rating = response.xpath(self.filters[10]).extract_first()
        audit_rating_val = response.xpath(self.filters[11]).extract()
        country = response.xpath(self.filters[12]).extract_first()
        country_val = response.xpath(self.filters[13]).extract()
        form_data = {
            SQFI_audit_type: SQFI_audit_type_val,
            food_sector_categories: food_sector_categories_val,
            audit_rating: audit_rating_val,
            country: country_val,
        }
        return form_data


class SuppliersAssessmentSpider72(SuppliersAssessmentSpider80):
    """
    Spider for SQFI audit type 'SQF Food Safety Audit Edition 7.2'
    """
    name = "suppliers_assessment_7_2"
    sqf_food = 'SQF Food Safety Audit Edition 7.2'
