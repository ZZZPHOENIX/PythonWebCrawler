#__author: ZhangWP
#date : 2018/8/8
#爬取失败

import urllib.request
import urllib.error
import re

header = ('user-agent',"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36")
opener = urllib.request.build_opener()
opener.add_handlers=[header]
urllib.request.install_opener(opener)

def get_rate(page):
    try:
        url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=546318951474&spuId=795023941&sellerId=1860270913&order=3&currentPage='+str(page)+'&append=0&content=1&tagId=&posi=&needFold=0&_ksTS=1533702509498_1808&callback=jsonp1809'
        data = urllib.request.urlopen(url).read().decode('utf-8',"ignore")
        pattern = '"rateContent":"(.*?)"'
        comments = re.findall(pattern,data)
        file = open('TaobaoComments.txt','w')
        for comment in comments:
            file.write(comment+"\n")
        #print(5)
        file.close()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    except Exception as e2:
        print(e2)

get_rate(1)