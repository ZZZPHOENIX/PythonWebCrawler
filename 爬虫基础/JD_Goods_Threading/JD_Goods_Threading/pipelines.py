# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JdGoodsThreadingPipeline(object):
    global i
    i = 1

    def process_item(self, item, spider):
        database = pymysql.connect(host='127.0.0.1', user='root', password='Zwp0816...', db='JD_Goods')
        # print("index" + str(i))
        name = item['name'][0]
        # print(name)
        price = item['price']
        # print(price)
        comment_count = item['comment_count']
        # print(comment_count)
        comment_rate = item['comment_rate']
        # print(comment_rate)
        internalStorage = item['internalStorage']
        # print(internalStorage)
        cpuType = item['cpuType']
        # print(item['cpuType'])
        cpuModel = item['cpuModel']
        # print(item['cpuModel'])
        cpuSpeed = item['cpuSpeed']
        # print(item['cpuSpeed'])
        cpuCore = item['cpuCore']
        # print(item['cpuCore'])
        diskCapacity = item['diskCapacity']
        # print(item['diskCapacity'])
        SSD = item['SSD']
        # print(item['SSD'])
        GCtype = item['GCtype']
        # print(item['GCtype'])
        GCcore = item['GCcore']
        # print(item['GCcore'])
        GCcapacity = item['GCcapacity']
        # print(item['GCcapacity'])
        size = item['size']
        # print(item['size'])
        weight = item['weight']
        # print(item['weight'])
        link = item['link']
        sql = "insert into pcInfo values('" + name + "','" + price + "','" + comment_count + "','" + comment_rate + "','" + internalStorage + "','" + cpuType + "','" + cpuModel + "','" + cpuSpeed + "','" + cpuCore + "','" + diskCapacity + "','" + SSD + "','" + GCtype + "','" + GCcore + "','" + GCcapacity + "','" + size + "','" + weight + "','" + link + "');"
        # print(1)
        database.query(sql)
        commit = "commit;"
        # print(2)
        database.query(commit)
        global i
        print("\t\t第" + str(i) + "个商品处理完成\n")
        i = i + 1
        database.close()
        return item