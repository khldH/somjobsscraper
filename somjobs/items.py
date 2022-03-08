import scrapy


class SomJobsItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    category = scrapy.Field()
    posted_date = scrapy.Field()
    # expires = scrapy.Field()
    url = scrapy.Field()
    # short_url = scrapy.Field()
    location = scrapy.Field()
    organization = scrapy.Field()
    source = scrapy.Field()
