from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from somjobs.spiders.job import JobSpider

settings = get_project_settings()


if __name__ == "__main__":
    process = CrawlerProcess(settings=settings)
    process.crawl(JobSpider)
    process.start()
