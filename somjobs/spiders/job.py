import scrapy
import logging
import uuid

from somjobs.items import SomJobsItem

logger = logging.getLogger(__name__)


class JobSpider(scrapy.Spider):
    name = 'job'

    start_urls = ['https://somalijobs.net/#open']

    def parse(self, response):
        for quote in response.css('div.job_listing-about'):
            yield {
                'organization': quote.css('div.job_listing-company ::text').get(),
                'title': quote.css('h3.job_listing-title ::text').get(),
                'url': quote.css('h3 a ::attr(href)').get(),
                'category': quote.css('div.details a ::text').get(),
                'posted_date': quote.css('div.details span.spaced-right ::text').get(),
                'type': quote.css('div.mixed ::text').get()
            }


    # def parse(self, response):
    #     job_links = response.css('h3 a ::attr(href)')
    #     yield from response.follow_all(job_links, self.parse_job)
    #
    # def parse_job(self, response):
    #     item = SomJobsItem()
    #
    #     def extract_with_css(query):
    #         return response.css(query).get(default='').strip()
    #
    #     item['id'] = str(uuid.uuid4())
    #     item['title'] = extract_with_css('h1.title::text')
    #     # item['job_type'] = extract_with_css('.jbtype ::text')
    #     item['category'] = extract_with_css('.top-style li a ::text')
    #     item['posted_date'] = response.xpath('//*[@id="mainContent"]/div[3]/ul/li[2]/text()').get()
    #     # item['expires'] = response.xpath('//*[@id="mainContent"]/div[3]/ul/li[3]/text()').get()
    #     item['url'] = response.url
    #     item['country'] = 'Somalia'
    #     item['city'] = 'Somalia'
    #     # item['organization'] = self.org  # response.xpath('//*[@id="mainContent"]/ol/li[1]/div[3]/div[1]/div').get()
    #     item['source'] = 'Somali jobs'
    #
    #     yield item
