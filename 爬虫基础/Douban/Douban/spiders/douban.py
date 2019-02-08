# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import urllib.request

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36'}
    '''
    start_urls = ['http://douban.com/']
    '''

    def start_requests(self):
        return [Request("https://accounts.douban.com/login",callback=self.parse,meta={'cookiejar':1})]

    def parse(self, response):
        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()
        url = "https://accounts.douban.com/login"
        if len(captcha) > 0:
            print("此时有验证码")
            localpath = "D:/文件/学习/Python/网络爬虫/Douban/captcha_img.jpg"
            urllib.request.urlretrieve(captcha[0],filename=localpath)
            captcha_solution = input("查看本地验证码图片并输入验证码 >>")
            data = {
                'form_email': '18190687825',
                'form_password': 'Zwp0816...',
                'captcha-solution':captcha_solution,
                'redir': 'https://www.douban.com/people/151255139/',
            }
        else:
            print("此时没有验证码")
            data = {
                'form_email': '18190687825',
                'form_password': 'Zwp0816...',
                'redir': 'https://www.douban.com/people/151255139/'
            }
        print('登陆中----')

        return [FormRequest.from_response(response,
                                          meta={'cookiejar':response.meta["cookiejar"]},
                                          headers=self.header,
                                          formdata=data,
                                          callback=self.next,
                                          )]

    def next(self,response):
        print("此时已经登陆成功并爬取完成个人中心数据")
        personal_centere = response.xpath("//title/text()").extract()
        comments = response.xpath('//li[@class="mbtrdot comment-item"]/text()').extract()
        print(personal_centere[0])
        print(comments[0])