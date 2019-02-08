# -*- coding: utf-8 -*-
import scrapy
from Dangdang.items import DangdangItem
from scrapy.http import Request
import pymysql
import re

class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/pg1-cp01.54.00.00.00.00.html']
    def __init__(self):
        database = pymysql.connect(host='127.0.0.1',user='root',password='Zwp0816...',db='dangdang_tech_books')
        drop_table = "drop table if exists bookinfo;"
        create_table = "create table bookinfo(title varchar(100), link varchar(100) primary key , comment int, price float);"
        database.query(drop_table)
        database.query(create_table)
        database.close()

    def parse(self, response):
        item = DangdangItem()
        item['title'] = response.xpath('//a[@name="itemlist-picture"]/@title').extract()
        #print(item['title'])
        item['link'] = response.xpath('//a[@name="itemlist-picture"]/@href').extract()
        item['comment'] = response.xpath('//a[@dd_name="单品评论"]/text()').extract()
        for i in range(0,len(item['comment'])):
            item['comment'][i] = int(item['comment'][i].replace("条评论",''))
        item['price'] = response.xpath('//span[@class="search_now_price"]/text()').extract()
        for i in range(0, len(item['price'])):
            item['price'][i] = float(re.findall('[0-9.].*',item['price'][i].replace('&yen;', ''))[0])
        yield item
        for i in range(2,101):
            url = 'http://category.dangdang.com/pg'+str(i)+'-cp01.54.00.00.00.00.html'
            yield Request(url,callback=self.parse)


