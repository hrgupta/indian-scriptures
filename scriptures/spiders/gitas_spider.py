import re

import scrapy
from scrapy.crawler import CrawlerProcess

# This class is the main spider class. It will crawl the main website.


class MantraSpider(scrapy.Spider):
    name = "mantraspider"
    start_urls = ["https://old.gitasupersite.in/minigita/texts"]

    def parse(self, response):

        links = response.css("div.field-item.even a::attr(href)").getall()
        for url in links:
            yield response.follow(url, callback=self.parse_mantra)

    # Function to get all the mantras from the website
    def parse_mantra(self, response):

        for mantra in response.css("div.views-field.views-field-body"):
            shloka = mantra.css("font::text").getall()

        # remove new-line chars from string
        shloka = list(map(lambda x: x.replace("\n", ""), shloka))
        # remove empty strings
        shloka = list(filter(lambda x: x != "", shloka))

        yield {"title": response.css("h1.page-title::text").get(), "mantra": shloka}

        try:
            next_page = response.css("p.navigation_block a::attr(href)")[2].get()
        except IndexError:
            next_page = response.css("p.navigation_block a::attr(href)")[1].get()

        pages = re.findall(r"\d+", next_page)
        flag = self.check_start_page(pages)

        if not flag:
            yield response.follow(next_page, callback=self.parse_mantra)

    def check_start_page(self, page):
        ele = 1
        chk = True
        # Comparing each element with first item
        for item in page:
            if ele != item:
                chk = False
                break

        if chk is True:
            return True
        else:
            return False


process = CrawlerProcess(
    settings={
        "FEEDS": {
            "../../data/raw/gitas/gitas.csv": {"format": "csv", "overwrite": True},
        },
        "USER_AGENT": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        ),
    }
)
process.crawl(MantraSpider)
process.start()
