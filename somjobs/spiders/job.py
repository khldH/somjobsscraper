import scrapy


class JobSpider(scrapy.Spider):
    name = 'job'

    start_urls = ['https://somalijobs.net/#open']

    def parse(self, response):
        job_links = response.css('h3 a ::attr(href)')
        yield from response.follow_all(job_links, self.parse_job)

    def parse_job(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'title': extract_with_css('h1.title::text'),
            'job_type': extract_with_css('.jbtype ::text'),
            'category': extract_with_css('.top-style li a ::text'),
            'posted_date': response.xpath('//*[@id="mainContent"]/div[3]/ul/li[2]/text()').get(),
            'expires': response.xpath('//*[@id="mainContent"]/div[3]/ul/li[3]/text()').get()
        }
