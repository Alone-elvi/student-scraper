import scrapy
from icecream import ic

class KaspiSpider(scrapy.Spider):
    name = 'kaspi'
    allowed_domains = ['kaspi.kz']
    notebooks_url = 'c/notebooks/'
    start_urls = ['https://kaspi.kz/shop/'+notebooks_url]

    def parse(self, response):
        for a in response.css('div.item-card__name'):
            ic(a, a.xpath('.//a/@href').get())
            yield {'url': a.xpath('.//a/@href').get()}