import scrapy
from scrapy.crawler import CrawlerProcess

# This class is the main spider class. It will crawl the main website.
class MantraSpider(scrapy.Spider):
    name = "mantraspider"
    
    def start_requests(self):
        start_urls = [
        'https://www.upanishads.iitk.ac.in/aitereya',
        'https://www.upanishads.iitk.ac.in/isavasya',
        'https://www.upanishads.iitk.ac.in/karika',
        'https://www.upanishads.iitk.ac.in/katha',
        'https://www.upanishads.iitk.ac.in/kena',
        'https://www.upanishads.iitk.ac.in/mundaka',
        'https://www.upanishads.iitk.ac.in/mandukya',
        'https://www.upanishads.iitk.ac.in/prasna',
        'https://www.upanishads.iitk.ac.in/brihadaranyaka',
        'https://www.upanishads.iitk.ac.in/svetashvatra',
        'https://www.upanishads.iitk.ac.in/taittiriya'
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_mantra)

    # Function to get all the mantras from the website
    def parse_mantra(self, response):

        for mantra in response.css('div.views-field.views-field-body'):
            yield {
                'title': response.css('h1.page-title::text').get(),
                'mantra': mantra.css('font::text').getall(),
            }

        first_page = response.css('p.navigation_block a::attr(href)')[0].get()
        next_page = response.css('p.navigation_block a::attr(href)')[3].get()
        if next_page != first_page:
            yield response.follow(next_page, callback=self.parse_mantra)

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'csv',
    'FEED_URI': '../../data/raw/upanishads.csv'
})
process.crawl(MantraSpider)
process.start()