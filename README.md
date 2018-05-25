# LightCrawler

This is a Scrapy project to:
* scrape data from [Bancor](https://www.bancor.network/discover) for bid and ask prices
* scrape data from the results [SQF Institute](https://www.sqfi.com/suppliers/assessment-database/public-search/)
* save scrape results into a 2D array CSV, XLSX

## 1. Requirements

* **Python** version >= 3.5

##### 1.1 Install requirements packages

```
$ pip3 install -r requirements.txt
```

## 2. Spiders

This project contains three spiders and you can list them using the `list` command:

```
~/LightCrawler$ scrapy list
```

* **bancor_prices** Spider for [Bancor](https://www.bancor.network/discover)
* **suppliers_assessment_8_0** Spider for [SQF Institute](https://www.sqfi.com/suppliers/assessment-database/public-search/) SQFI audit type: SQF Food Safety Audit Edition 8.0
* **suppliers_assessment_7_2** Spider for [SQF Institute](https://www.sqfi.com/suppliers/assessment-database/public-search/) SQFI audit type: SQF Food Safety Audit Edition 7.2

## Running the spiders

You can run a spider using the `scrapy crawl` command, such as:

```
~/LightCrawler$ scrapy crawl bancor_prices
~/LightCrawler$ scrapy crawl suppliers_assessment_8_0
~/LightCrawler$ scrapy crawl suppliers_assessment_7_2
```

## Scraping results

You can see the result files in the "media" sub-directory of project's root directory

# python_scrapy_parser_ligthcrawler
