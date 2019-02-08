# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdGoodsThreadingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 商品名称
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 评论数
    comment_count = scrapy.Field()
    # 好评度
    comment_rate = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 内存
    internalStorage = scrapy.Field()
    # CPU类型
    cpuType = scrapy.Field()
    # CPU型号
    cpuModel = scrapy.Field()
    # CPU速度
    cpuSpeed = scrapy.Field()
    # CPU核心
    cpuCore = scrapy.Field()
    # 硬盘容量
    diskCapacity = scrapy.Field()
    # 固态硬盘
    SSD = scrapy.Field()
    # 显卡类型
    GCtype = scrapy.Field()
    # 显示芯片
    GCcore = scrapy.Field()
    # 显存容量
    GCcapacity = scrapy.Field()
    # 尺寸
    size = scrapy.Field()
    # 重量
    weight = scrapy.Field()
