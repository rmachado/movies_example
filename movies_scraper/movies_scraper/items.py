# -*- coding: utf-8 -*-
import scrapy

class MovieItem(scrapy.Item):
    title = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    description = scrapy.Field()
    storyline = scrapy.Field()
    cover = scrapy.Field()
    genres = scrapy.Field()
    website = scrapy.Field()
    score = scrapy.Field()
    num_reviews = scrapy.Field()
    directors = scrapy.Field()
    actors = scrapy.Field()