import scrapy
import logging
from scrapy.shell import inspect_response

# command line: scrapy crawl countries -o population_dataset.json --> becomes a json file
# command line: scrapy crawl countries -o population_dataset.csv  --> becomes a csv file
# command line: scrapy crawl countries -o population_dataset.xml  --> becomes a xml file

# the following command line tells scrapy to execute only the parse_country function
# command line: scrapy parse --spider=countries -c parse_country --meta='{"country_name":"China"}' https://www.worldometers.info/world-population/china-population/

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

            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

    def parse_country(self, response):
        # this is like a breakpoint, it becomes interactive
        # inspect_response(response, self) 
        
        name = response.request.meta['country_name']
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
                'country_name': name,
                'year': year,
                'population': population
            }