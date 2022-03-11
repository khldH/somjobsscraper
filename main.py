from scrapy.crawler import CrawlerProcess
from somjobs.spiders.job import JobSpider
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


if __name__ == "__main__":
    process = CrawlerProcess(settings=settings)
    process.crawl(JobSpider)
    process.start()
