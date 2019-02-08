# -*- coding: utf-8 -*-
import scrapy
from TianshanCourses.items import TianshancoursesItem
from scrapy.http import Request

class LessonSpider(scrapy.Spider):
    name = 'lesson'
    allowed_domains = ['hellobi.com']
    start_urls = ['http://edu.hellobi.com/course/1']

    def parse(self, response):
        item = TianshancoursesItem()
        item['title'] = response.xpath('//ol[@class="breadcrumb"]/li[@class="active"]/text()').extract()
        item['link'] = response.xpath('//input[@name="redirect_url"]/@value').extract()
        item['stu'] = response.xpath('//span[@class="course-view"]/text()').extract()
        #print(item['title'])
        #print(item['stu'])
        #print(item['link'])
        yield item
        for i in range(2,289):
            url = "http://edu.hellobi.com/course/" + str(i)
            yield Request(url, callback=self.parse)