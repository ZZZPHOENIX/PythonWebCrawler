# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
global count
count = 1
class DangdangPipeline(object):
    def process_item(self, item, spider):

        database = pymysql.connect(host='127.0.0.1',user='root',password='Zwp0816...',db='dangdang_tech_books')

        for i in range(0,len(item['title'])):
            title = item['title'][i]
            link = item['link'][i]
            comment = item['comment'][i]
            price = item['price'][i]
            sql = "insert into bookinfo(title,link,comment,price) values('%s','%s','%d','%lf');"%(title, link, comment, price)
            database.query(sql)
            database.commit()
            global count
            print("第"+str(count)+"本书写入完成！")
            count += 1
        database.close()
        return item
