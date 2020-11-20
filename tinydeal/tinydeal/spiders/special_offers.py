import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com']
    start_urls = ['https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html?disp_order=18/']

    def parse(self, response):
        pass
