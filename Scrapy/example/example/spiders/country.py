# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from example.items import ExampleItem


class CountrySpider(CrawlSpider):
    name = 'country'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/']

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow='/places/default/index/', deny='/places/default/user/'), follow=True),
        Rule(LinkExtractor(allow='/places/default/view/', deny='/places/default/user/'), callback='parse_item')
    )

    def parse_item(self, response):
        # i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
        items = ExampleItem()
        name = 'tr#places_country__row td.w2p_fw::text'
        population = 'tr#places_population__row td.w2p_fw::text'
        items['name'] = response.css(name).extract()
        items['population'] = response.css(population).extract()
        return items
