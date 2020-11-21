import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers/']

    def parse(self, response):
        products = response.xpath('//div[@id="product-lists"]/div')
        for product in products:
            if product.xpath('.//div[@class="p-title"]/a/text()').get() is None:
                continue
            yield {
                'product_name': product.xpath('.//div[@class="p-title"]/a/text()').get().replace(' ', '').replace('\n', ''),
                'product_url': product.xpath('.//div[@class="product-img-outer"]/a/@href').get(),
                'product_image_url': product.xpath('.//div[@class="product-img-outer"]//img/@data-src').get(),
                'product_price': product.xpath('.//div[@class="p-price"]//span/text()').get()
            }

            next_page = response.xpath('(//ul[@class="pagination"])[1]/li[position() = last()]/a/@href').get()
            
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)
