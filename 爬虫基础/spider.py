from scrapy.spiders import Spider
class FirstSpider(Spider):
    #设置爬虫名字
    name = "first"
    #控制允许爬取的域名
    allowed_domains = ["baiud.com"]
    #起始域名
    start_urls = ["http://www.baidu.com",]
    #回调方法--运行后调用该方法
    def parse(self,response):#response为爬取后的响应
        pass
