from scrapy.crawler import CrawlerProcess
from somjobs.spiders.job import JobSpider

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(JobSpider)
    process.start()
