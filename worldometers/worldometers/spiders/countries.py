import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries' # must be unique across spiders
    allowed_domains = ['www.worldometers.info']  # stops the spider not to visit to facebook or other sites, and don't put https in the front
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')
        for country in countries:
            name = country.xpath('.//text()').getall()
            link = country.xpath('.//@href').getall()

            yield {
                'country_name': name,
                'country_link': link
            }
