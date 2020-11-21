import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.cigabuy.com/consumer-electronics-c-56_75-pg-1.html', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        })

    def parse(self, response):
        for product in response.xpath('//div[@class="p_box_wrapper"]/div'):
            yield {
                'title': product.xpath('.//a[@class="p_box_title"]/text()').get(),
                'url': response.urljoin(product.xpath('.//a[@class="p_box_title"]/@href').get()),
                'discounted_priced': product.xpath('.//div[@class="p_box_price cf"]/span[1]/text()').get(),
                'original_priced': product.xpath('.//div[@class="p_box_price cf"]/span[2]/text()').get(),
                'User-Agent': response.request.headers['User-Agent']
            }
        
        next_page = response.xpath('//a[@class="nextPage"]/@href').get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        })
