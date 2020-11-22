import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        # allow=r'Items/' if the link contains 'Items/', then follow the link
        # deny=r'Items/' if the link contains 'Items/', do not follow the link
        # Rule(LinkExtractor(restrict_xpath=('//a[@class="active"])), callback='parse_item', follow=True), --> follow all the <a> elements that have the class == "active"
        Rule(LinkExtractor(restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="lister-page-next next-page"])[1]'), process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath('//div[@class="title_wrapper"]/h1/text()').get(),
            'year': response.xpath('//span[@id="titleYear"]/a/text()').get(),
            'duration': response.xpath('normalize-space((//time)[1]/text())').get(),
            'genre': response.xpath('//div[@class="subtext"]/a[1]/text()').get(),
            'rating': response.xpath('//div[@class="ratingValue"]/strong/span/text()').get(),
            'movie_url': response.url,
            'user-agent': response.request.headers['User-Agent']
        }
