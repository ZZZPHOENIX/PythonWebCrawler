# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TianshancoursesPipeline(object):
    def __init__(self):
        self.file = open('D:/文件/学习/Python/网络爬虫/TianshanCourses/data.txt','a')
    def process_item(self, item, spider):
        print(item['title'])
        print(item['stu'])
        print(item['link'])
        print('-------------')
        self.file.write(item['title'][0]+'\n'+item['stu'][0]+'\n'+item['link'][0]+'----------------'+'\n')
        return item
    def close_spider(self):
        self.file.close()