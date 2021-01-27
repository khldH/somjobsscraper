import scrapy

from somjobs.items import SomJobsItem


class JobSpider(scrapy.Spider):
    name = 'job'

    start_urls = ['https://somalijobs.net/#open']

    def parse(self, response):
        job_links = response.css('h3 a ::attr(href)')
        yield from response.follow_all(job_links, self.parse_job)

    def parse_job(self, response):
        item = SomJobsItem()

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        item['title'] = extract_with_css('h1.title::text')
        item['job_type'] = extract_with_css('.jbtype ::text')
        item['category'] = extract_with_css('.top-style li a ::text')
        item['posted_date'] = response.xpath('//*[@id="mainContent"]/div[3]/ul/li[2]/text()').get()
        item['expires'] = response.xpath('//*[@id="mainContent"]/div[3]/ul/li[3]/text()').get()
        item['link'] = response.url

        yield item

