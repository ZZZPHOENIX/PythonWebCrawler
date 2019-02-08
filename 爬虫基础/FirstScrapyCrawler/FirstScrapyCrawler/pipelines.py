# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FirstscrapycrawlerPipeline(object):
    def process_item(self, item, spider):
        '''
        for url in item['urls']:
            url = 'http://www.qiushibaike.com' + url

        for i in range(0,len(item["content"])):
            print('------------------')
            print(item['urls'][i])
            print(item['content'][i])

        return item
        '''
        pass