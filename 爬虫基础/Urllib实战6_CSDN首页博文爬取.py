#__author: ZhangWP
#date : 2018/8/7
import urllib.request
import urllib.error
import re

opener = urllib.request.build_opener()
opener.add_handlers=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36')]
urllib.request.install_opener(opener)   #添加opener为全局，之后利用urllib.request.urlopen()时会是已更改的header
start_url = 'http://www.csdn.net/nav/newarticles'
page = opener.open(start_url).read()


url_pattern = 'href="(.*?)" target="_blank" data-track-click'
article_urls = re.findall(url_pattern, page.decode('utf-8'))
#print(article_urls)
title_pattern = '<h1 class="title-article">(.*?)</h1>'
for url in article_urls:
    try:
        article = urllib.request.urlopen(url).read()
        #article = opener.open(url).read()
        title = re.findall(title_pattern,article.decode('utf-8','ignore'))[0]
        print(title)
        addr = 'D:/文件/学习/Python/网络爬虫/CSDN_articles/'+title + '.html'
        urllib.request.urlretrieve(url,filename=addr)
    except urllib.error.URLError as error:
        if hasattr(error,"code"):
            print(error.code)
        if hasattr(error,"reason"):
            print(error.reason)
    except Exception as error2:
        print(error2)
        continue

