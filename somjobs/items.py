import scrapy


class SomJobsItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    # job_type = scrapy.Field()
    category = scrapy.Field()
    posted_date = scrapy.Field()
    # expires = scrapy.Field()
    url = scrapy.Field()
    # short_url = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    organization = scrapy.Field()
    source = scrapy.Field()
