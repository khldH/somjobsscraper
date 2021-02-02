import scrapy


class SomJobsItem(scrapy.Item):
    title = scrapy.Field()
    job_type = scrapy.Field()
    category = scrapy.Field()
    posted_date = scrapy.Field()
    expires = scrapy.Field()
    link = scrapy.Field()
    short_url = scrapy.Field()
