import requests
import re
import datetime
from bs4 import BeautifulSoup
from multiprocessing import Process
from multiprocessing import Manager
import sys

sys.setrecursionlimit(1000000)


class NovelCrawler():
    def __init__(self, start_url):
        """
        初始化
        :param start_url:小说主界面
        """
        #页面计数
        self.count = 0
        #基本地址
        self.base_url = re.compile('(.*/)').findall(start_url)[0]
        #目标文件
        name = start_url.split('/')[-2]
        self.file = open('./%s.txt' % name, 'a')
        #程序开始时间
        self.startTime = datetime.datetime.now()

        startPage = BeautifulSoup(requests.get(start_url).text, 'lxml')
        chapters = startPage.select('#list ul li a')
        #[(章节名，章节相对地址),]
        self.chapters = [(chapter.string, chapter['href']) for chapter in chapters]

    def timing(self):
        """
        计时
        :return:程序运行时间
        """
        endTime = datetime.datetime.now()
        return (endTime - self.startTime)

    def crawl(self):
        """
        爬取单个页面
        :return:
        """
        info = self.chapters.pop(0)
        title = info[0]
        url = info[1]
        self.count += 1
        url = self.base_url + url
        page_source = requests.get(url).text
        try:
            content = re.compile('<div id="content">(.*?)</div>').findall(page_source)[0]
            content = content.replace('<p>', '')
            content = content.replace('</p>', '\n')
        except:
            print("错误！"+url)

        self.file.write("-"*50 + '\n' + title + '\n\n' + content)
        print("第%s页写入完成！" % self.count)

    def run(self):
        """
        运行爬虫
        :return:
        """
        while self.chapters:
            self.crawl()
        print("爬取完毕！共耗时%s" % self.timing())

if __name__ == '__main__':
    crawler = NovelCrawler('https://www.qkshu.com/book/doupocangqiong/')
    crawler.run()