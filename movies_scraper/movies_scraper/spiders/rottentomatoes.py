# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from movies_scraper.items import MovieItem


class RottentomatoesSpider(scrapy.Spider):
    name = "rottentomatoes"
    allowed_domains = ["www.rottentomatoes.com"]
    start_urls = ['https://www.rottentomatoes.com/']

    def parse(self, response):
        current_year = datetime.now().year
        year_url = 'https://www.rottentomatoes.com/top/bestofrt/?year={0}'
        years = self.settings.getint('YEARS_TO_SCRAPE')

        for year in range(current_year - years, current_year + 1):
            yield scrapy.Request(year_url.format(year), callback=self.parse_list)

    def parse_list(self, response):
        sel = scrapy.Selector(response=response)
        reviews = sel.xpath('//table[@class="table"]//tr')

        for review in reviews[1:]:
            movie = MovieItem()

            movie["website"] = "Rotten Tomatoes"
            title = review.xpath('.//td/a/text()').extract_first()
            print(title)
            movie["title"], movie["year"] = re.search(r'(.+) \((\d+)\)', title).groups()
            movie["score"] = review.xpath('.//span[@class="tMeterScore"]/text()').extract_first()
            movie["num_reviews"] = review.xpath('.//td[contains(@class,"right")]/text()').extract_first()

            yield movie