# -*- coding: utf-8 -*-
import scrapy
from JD_goods.items import JdGoodsItem
from scrapy.http import Request,Response
import urllib.request
import urllib.error
import re
#import json
import random
import pymysql
import winsound

class GoodsSpider(scrapy.Spider):
    name = 'goods'
    allowed_domains = ['jd.com']
    #设置全局变量index,用于方法内遍历网页
    global index
    index = 0
    def __init__(self):
        database = pymysql.connect(host='127.0.0.1',user='root',password='Zwp0816...',db='JD_Goods')
        drop_table = "drop table if exists pcInfo;"
        create_table = "create table pcInfo(名称 varchar(100), 价格 varchar(100), 评论数 varchar(15), 好评度 varchar(10), 内存 varchar(100), CPU类型 varchar(100), CPU型号 varchar(100), CPU速度 varchar(100), CPU核心 varchar(100), 硬盘容量 varchar(100), 固态硬盘 varchar(100), 显卡类型 varchar(100), 显示芯片 varchar(100), 显存容量 varchar(100), 尺寸 varchar(100), 重量 varchar(100), 链接 varchar(100));"
        database.query(drop_table)
        database.query(create_table)
        database.close()

    def start_requests(self):
        self.links = []
        #获取单个商品主页面URL
        print("\n正在获取并处理商品链接...\n")
        #TOTAL为总页数
        url = "https://list.jd.com/list.html?cat=670,671,672&page=1&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main"
        TOTAL = int(re.findall('<em>共<b>(.*?)</b>',urllib.request.urlopen(url).read().decode('utf-8','ignore'))[0])
        #print(TOTAL)
        for i in range(1, 3):
            try:
                url = "https://list.jd.com/list.html?cat=670,671,672&page=" + str(i) + "&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main"
                page = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
                self.links += re.compile('<a target="_blank" title="" href="(.*?)">').findall(page)
                print(slinks)
                print("\t\t第"+str(i)+"页处理完成\n")
                #print(len(self.links))
            except urllib.error.URLError as e:
                if hasattr(e, 'code'):
                    print(e.code)
                if hasattr(e, 'reason'):
                    print(e.reason)
                continue
            except Exception as e:
                print(e)
                continue
        #print(self.links)
        #处理商品URL
        for i in range(0,len(self.links)):
            self.links[i] = 'https:' + self.links[i]
        print("\n所有商品链接获取并处理完成！\n")
        #设置头信息
        ua = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}

        global index
        #print(self.links[index])
        yield Request(self.links[index],headers=ua)

    def parse(self, response):
        global index
        data = JdGoodsItem()
        data['name'] = response.xpath('//img[@id="spec-img"]/@alt').extract()
        data['link'] = self.links[index]
        index += 1
        #获取商品价格
        good_id = re.findall('.*/(.*?).html',data['link'])[0]
        price_url = 'https://p.3.cn/prices/mgets?pduid=' + str(random.randint(100000, 999999)) + '&skuIds=J_' + good_id+ '&ext=11100000&source=item-pc'
        print(price_url)
        content = urllib.request.urlopen(price_url).read().decode('utf-8', 'ignore')
        data['price'] = re.findall('"p":"(.*?)"',content)[0]

        #获取评论数及好评度
        comment_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv' + str(random.randint(1000, 9999)) + '&productId=' + good_id + '&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        comment_data = urllib.request.urlopen(comment_url).read().decode('utf-8', 'ignore')
        data['comment_count'] = re.findall('"commentCountStr":"(.*?)"', comment_data)[0]
        data['comment_rate'] = re.findall('"goodRateShow":(.*?),', comment_data)[0] + "%"
        #print(data['comment_rate'])

        page_content = urllib.request.urlopen(data['link']).read().decode('gbk','ignore')

        pattern1 = '<dt>内存容量</dt>.*?<dd>(.*?)</dd>'
        pattern2 = '<dt>内存类型</dt>.*?<dd>(.*?)</dd>'
        result1 = re.findall(pattern1,page_content,re.S)
        result2 = re.findall(pattern2,page_content,re.S)
        if len(result1) > 0 and len(result2) > 0:
            data['internalStorage'] = (result1[0]+'    '+result2[0])
        elif len(result1) > 0 and len(result2) == 0:
            data['internalStorage'] = result1[0]
        elif len(result2) > 0 and len(result1) == 0:
            data['internalStorage'] = result2[0]
        else:
            data['internalStorage'] = ' '

        pattern = '<dt>CPU类型</dt><dd>(.*?)</dd>'
        result = re.findall(pattern,page_content)
        if len(result) > 0:
            data['cpuType'] = result[0]
        else:
            data['cpuType'] = ' '


        pattern = '<dt>CPU型号</dt><dd>(.*?)</dd>'
        result = re.findall(pattern, page_content)
        if len(result) > 0:
            data['cpuModel'] = result[0]
        else:
            data['cpuModel'] = ' '

        pattern = '<dt>CPU速度</dt><dd>(.*?)</dd>'
        result = re.findall(pattern,page_content)
        if len(result) > 0:
            data['cpuSpeed'] = result[0]
        else:
            data['cpuSpeed'] = ' '

        pattern = '<dt>核心</dt><dd>(.*?)</dd>'
        result = re.findall(pattern,page_content)
        if len(result) > 0:
            data['cpuCore'] = result[0]
        else:
            data['cpuCore'] = ' '

        pattern = '<dt>硬盘容量</dt><dd>(.*?)</dd>'
        result = re.findall(pattern,page_content)
        if len(result) > 0:
            data['diskCapacity'] = result[0]
        else:
            data['diskCapacity'] = ' '

        pattern = '<dt>固态硬盘</dt><dd>(.*?)</dd>'
        result = re.findall(pattern, page_content)
        if len(result) > 0:
            data['SSD'] = result[0]
        else:
            data['SSD'] = ' '

        pattern = '<dt>类型</dt><dd>(.*?)</dd>'
        result = re.findall(pattern, page_content)
        if len(result) > 0:
            data['GCtype'] = result[0]
        else:
            data['GCtype'] = ' '

        pattern = '<dt>显示芯片</dt><dd>(.*?)</dd>'
        result = re.findall(pattern, page_content)
        if len(result) > 0:
            data['GCcore'] = result[0]
        else:
            data['GCcore'] = ' '

        pattern = '<dt>显存容量</dt><dd>(.*?)</dd>'
        result = re.findall(pattern, page_content)
        if len(result) > 0:
            data['GCcapacity'] = result[0]
        else:
            data['GCcapacity'] = ' '

        pattern = '<dt>尺寸</dt><dd>(.*?)</dd>'
        result = re.findall(pattern, page_content)
        if len(result) > 0:
            data['size'] = result[0]
        else:
            data['size'] = ' '

        pattern = '<dt>净重</dt><dd>(.*?)</dd>'
        result = re.findall(pattern, page_content)
        if len(result) > 0:
            data['weight'] = result[0]
        else:
            data['weight'] = ' '

        yield data
        for i in range(1,len(self.links)):
            url = self.links[i]
            yield Request(url, callback=self.parse)

