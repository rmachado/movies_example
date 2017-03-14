# -*- coding: utf-8 -*-
import scrapy
from movies_scraper.items import MovieItem


class ImdbSpider(scrapy.Spider):
    name = "IMDb"
    allowed_domains = ["www.imdb.com"]
    start_urls = ['http://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth_1']

    def parse(self, response):
        sel = scrapy.Selector(response=response)

        movies_urls = sel.css('.list .list_item h4 a::attr(href)').extract()

        for url in movies_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_movie)

    def parse_movie(self, response):
        sel = scrapy.Selector(response=response)
        movie = MovieItem()

        movie["website"] = self.name
        movie["title"] = sel.xpath('//h1[@itemprop="name"]/text()').extract_first()
        movie["year"] = sel.xpath('//span[@id="titleYear"]/a/text()').extract_first()
        movie["duration"] = sel.xpath('//time[@itemprop="duration"]/text()').extract_first()
        movie["genres"] = sel.xpath('//div[@class="subtext"]//span[@itemprop="genre"]/text()').extract()
        movie["score"] = sel.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
        movie["num_reviews"] = sel.xpath('//span[@itemprop="ratingCount"]/text()').extract_first()
        movie["description"] = sel.xpath('//div[@class="summary_text"]/text()').extract_first()
        movie["storyline"] = sel.xpath('//div[@id="titleStoryLine"]//div[@itemprop="description"]/p/text()').extract_first()
        movie["cover"] = sel.xpath('//div[@class="poster"]//img/@src').extract_first()
        movie["directors"] = sel.xpath('//span[@itemprop="director"]//span/text()').extract()
        movie["actors"] = sel.xpath('//span[@itemprop="actors"]//span/text()').extract()

        return movie
