import logging
import time

import scrapy
from scrapy import Request
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from scrapy_splash import SplashRequest

logger = logging.getLogger(__name__)

# handle infinite scroll
script = """
    function main(splash)
        local num_scrolls = 10
        local scroll_delay = 1.0
    
        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )
        assert(splash:go(splash.args.url))
        splash:wait(splash.args.wait)
    
        for _ = 1, num_scrolls do
            scroll_to(0, get_body_height())
            splash:wait(scroll_delay)
        end        
        return splash:html()
    end
"""


class JobSpider(scrapy.Spider):
    name = "somalijobs"
    custom_settings = {
        "FEEDS": {
            "scraped_jobs/somalijobs.json": {
                "format": "json",
                "encoding": "utf8",
                "overwrite": True,
            }
        },
        "ITEM_PIPELINES": {"somjobs.pipelines.SomJobsPipeline": 300},
        "LOG_LEVEL": "INFO",
    }

    def start_requests(self):
        url = "https://somalijobs.com/jobs"
        yield SplashRequest(
            url=url,
            endpoint="execute",
            callback=self.parse,
            args={"wait": 2, "lua_source": script},
        )

    def parse(self, response):
        jobs = response.css("a.job-middle-grid.m-jobs-lising1-container")
        for job in jobs:
            yield {
                "title": job.css("h4::text").get(),
                "posted_date": job.css("div.jmg-post-date span::text").get(),
                "organization": job.css(
                    "h4.jmg-company-title.job-listing-1-company::text"
                ).get(),
                "location": job.css("span.skl-3.job-listing-1-items").get(),
                "category": job.css("span.skl-2.job-listing-1-items").get(),
                "type": job.css("span.skl-6.job-listing-1-items").get(),
                "url": job.css("::attr(href)").get(),
            }


class UNJobsSpider(scrapy.Spider):
    name = "unjobs"

    custom_settings = {
        "FEEDS": {
            "scraped_jobs/unjobs.json": {
                "format": "json",
                "encoding": "utf8",
                "overwrite": True,
            }
        },
        "ITEM_PIPELINES": {"somjobs.pipelines.UNJobsPipeline": 300},
        "LOG_LEVEL": "INFO",
    }

    def start_requests(self):
        url = "https://unjobs.org/duty_stations/somalia"
        yield SplashRequest(
            url=url,
            endpoint="execute",
            callback=self.parse,
            args={"wait": 2, "lua_source": script},
        )

    def parse(self, response):
        jobs = response.css("article div.job")
        for job in jobs:
            yield {
                "title": job.css("a::text").get(),
                "posted_date": job.css("time::text").get(),
                "organization": job.css("div.job::text").get(),
                "location": "",
                "category": "",
                "type": "",
                "url": job.css("::attr(href)").get(),
            }


class ImpactpoolJobsSpider(scrapy.Spider):
    name = "impactpooljobs"
    custom_settings = {
        "FEEDS": {
            "scraped_jobs/impactpooljobs.json": {
                "format": "json",
                "encoding": "utf8",
                "overwrite": True,
            }
        },
        "ITEM_PIPELINES": {"somjobs.pipelines.ImpactpoolJobsPipeline": 300},
        "LOG_LEVEL": "INFO",
    }

    def start_requests(self):
        url = "https://www.impactpool.org/search?q=&countries%5B%5D=Somalia"
        yield SplashRequest(
            url=url,
            endpoint="execute",
            callback=self.parse,
            args={"wait": 2, "lua_source": script},
        )

    def parse(self, response):
        jobs = response.css("div.jobs-list div.job")
        for job in jobs:
            yield {
                "title": job.css("a::text").get(),
                "posted_date": job.css("span::text").get(),
                "organization": job.css("div.job-info").get(),
                "location": job.css("div.job-info").get(),
                "category": "",
                "type": "",
                "url": job.css("a.apply-link::attr(href)").get(),
            }


class WeWorkRemotelySpider(scrapy.Spider):
    name = "weworkremotely"
    start_urls = ["https://weworkremotely.com/categories/remote-customer-support-jobs#job-listings",
                  "https://weworkremotely.com/categories/remote-sales-and-marketing-jobs#job-listings",
                  "https://weworkremotely.com/categories/remote-management-and-finance-jobs#job-listings",
                  "https://weworkremotely.com/categories/remote-design-jobs#job-listings"]
    custom_settings = {
        "FEEDS": {
            "scraped_jobs/weworkremotely.json": {
                "format": "json",
                "encoding": "utf8",
                "overwrite": True,
            }
        },
        "ITEM_PIPELINES": {"somjobs.pipelines.WeWorkRemotelyPipeline": 300},
        "LOG_LEVEL": "INFO",
    }

    def start_requests(self):
        # url = "https://weworkremotely.com/remote-jobs/search?term=&button=&categories%5B%5D=7&categories%5B%5D=9" \
        #       "&categories%5B%5D=3&region%5B%5D=0"
        # url = "https://weworkremotely.com/remote-jobs/search?term=&button=&region%5B%5D=0"
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                endpoint="execute",
                callback=self.parse,
                args={"wait": 2, "lua_source": script},
            )

    def parse(self, response):
        jobs = response.css("article ul li a")
        for job in jobs:
            yield {
                "title": job.css('span.title::text').get(),
                "posted_date": job.css('span.date time::text').get(),
                "organization": job.css("span.company::text").get(),
                "location": job.css("span.region::text").get(),
                "category": response.url.split("categories/remote-")[1].split("-jobs")[0],
                "type": "",
                "url": job.css("::attr(href)").get(),
            }



# class RemoteOKSpider(scrapy.Spider):
#     name = "remoteok"
#     start_urls = ["https://remoteok.com/remote-customer-support-jobs?location=Worldwide"]
#     custom_settings = {
#         "FEEDS": {
#             "scraped_jobs/remoteok.json": {
#                 "format": "json",
#                 "encoding": "utf8",
#                 "overwrite": True,
#             }
#         },
#         "ITEM_PIPELINES": {"somjobs.pipelines.RemoteOKPipeline": 300},
#         "LOG_LEVEL": "INFO",
#     }
#
#     def start_requests(self):
#
#         for url in self.start_urls:
#             yield SplashRequest(
#                 url=url,
#                 endpoint="execute",
#                 callback=self.parse,
#                 args={"wait": 2, "lua_source": script},
#             )
#
#     def parse(self, response):
#         jobs = response.css("article ul li a")
#         for job in jobs:
#             yield {
#                 "title": job.css('span.title::text').get(),
#                 "posted_date": job.css('span.date time::text').get(),
#                 "organization": job.css("span.company::text").get(),
#                 "location": job.css("span.region::text").get(),
#                 "category": response.url.split("categories/remote-")[1].split("-jobs")[0],
#                 "type": "",
#                 "url": job.css("::attr(href)").get(),
#             }

