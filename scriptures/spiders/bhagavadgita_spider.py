import scrapy
from scrapy.crawler import CrawlerProcess

# This class is the main spider class. It will crawl the main website.


class MantraSpider(scrapy.Spider):
    name = "mantraspider"

    async def start(self):
        start_urls = [
            "https://old.gitasupersite.in/srimad",
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_mantra)

    # Function to get all the mantras from the website
    def parse_mantra(self, response):

        for mantra in response.css("div.views-field.views-field-body"):
            shloka = mantra.css("font::text").getall()

        # remove new-line chars from string
        shloka = list(map(lambda x: x.replace("\n", ""), shloka))

        # remove empty strings
        shloka = list(filter(lambda x: x != "", shloka))

        yield {"title": response.css("h1.page-title::text").get(), "mantra": shloka}

        first_page = response.css("p.navigation_block a::attr(href)")[0].get()
        next_page = response.css("p.navigation_block a::attr(href)")[2].get()
        if next_page != first_page:
            yield response.follow(next_page, callback=self.parse_mantra)


process = CrawlerProcess(
    settings={
        "FEEDS": {
            "../../data/raw/gitas/bhagavadgita.csv": {
                "format": "csv",
                "overwrite": True,
            },
        },
        "USER_AGENT": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        ),
    }
)
process.crawl(MantraSpider)
process.start()
