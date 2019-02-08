# -*- coding: utf-8 -*-
import scrapy
import re
from FirstScrapyCrawler.items import FirstscrapycrawlerItem
from scrapy.http import Request

class QiushibaikeSpider(scrapy.Spider):
    name = 'Qiushibaike'
    allowed_domains = ['jd.com']

    start_urls = ['https://item.jd.com/5225346.html']
    '''
    def start_requests(self):
        ua = {'user-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36"}
        yield Request('http://www.qiushibaike.com/',headers=ua)

    '''
   def parse(self, response):
       item = FirstscrapycrawlerItem()
       pattern = '<dd>(.*GB)</dd>'
       temp = response.xpath("//dd").extract()
       item['content'] = re.findall(pattern,temp)
       #item['urls'] = response.xpath("//a[@class='contentHerf']/@href").extract()
       print(item['content'])
       #print(len(item['urls']))
       yield item

