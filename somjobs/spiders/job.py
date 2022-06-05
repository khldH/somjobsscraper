import logging

import scrapy
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
    name = "job"

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
