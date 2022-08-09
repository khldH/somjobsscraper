from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from somjobs.spiders.job import ImpactpoolJobsSpider, JobSpider, UNJobsSpider

settings = get_project_settings()


def run_all_spiders():
    print("start crawler")
    process = CrawlerProcess(settings=settings)
    process.crawl(JobSpider)
    process.crawl(UNJobsSpider)
    process.crawl(ImpactpoolJobsSpider)
    process.start(stop_after_crawl=True)
