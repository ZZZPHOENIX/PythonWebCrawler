# -*- coding: utf-8 -*-
import scrapy
from JD_goods.items import JdGoodsItem
from scrapy.http import Response
from scrapy.http import Request
import urllib.request
import re
import json


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['jd.com']
    '''
    start_urls = ['http://item.jd.com/5225346.html']
    '''
    def start_requests(self):
        yield Request('http://item.jd.com/5225346.html')

    def parse(self, response):
        item = JdGoodsItem()
        item['link'] = Response._get_url(self)
        print(item['link'])
        yield item
