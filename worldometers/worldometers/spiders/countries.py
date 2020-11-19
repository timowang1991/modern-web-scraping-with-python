import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries' # must be unique across spiders
    allowed_domains = ['www.worldometers.info']  # stops the spider not to visit to facebook or other sites, and don't put https in the front
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')
        for country in countries:
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            # absolute_url = f"https://www.worldometers.info{link}"
            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url)

            yield response.follow(url=link)
