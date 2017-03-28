# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy
from movies_scraper.items import MovieItem


class MetacriticSpider(scrapy.Spider):
    name = "metacritic"
    allowed_domains = ["www.metacritic.com"]
    start_urls = ['http://www.metacritic.com/']

    def parse(self, response):
        current_year = datetime.now().year
        year_url = 'http://www.metacritic.com/browse/movies/score/metascore/year/filtered?year_selected={0}&sort=desc'
        years = self.settings.getint('YEARS_TO_SCRAPE')

        for year in range(current_year - years, current_year + 1):
            yield scrapy.Request(year_url.format(year), callback=self.parse_list)

    def parse_list(self, response):
        sel = scrapy.Selector(response=response)
        links = sel.xpath('//table[@class="list score"]//div[@class="title"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_movie)

    def parse_movie(self, response):
        sel = scrapy.Selector(response=response)
        movie = MovieItem()

        movie["website"] = "Metacritic"
        movie["title"] = sel.xpath('//div[contains(@class,"product_page_title")]/h1/text()').extract_first()
        movie["year"] = sel.xpath('//div[contains(@class,"product_page_title")]/span/text()').extract_first()
        movie["score"] = sel.xpath('//a[@class="metascore_anchor"]/span/text()').extract_first()
        movie["num_reviews"] = sel.xpath('//span[@class="score_description"]//span[@class="based_on"]/text()').extract_first()

        return movie
