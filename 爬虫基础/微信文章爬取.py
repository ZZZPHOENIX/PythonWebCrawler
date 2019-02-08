#__author: ZhangWP
#date : 2018/8/8
import urllib.error
import urllib.request
import re
import time

def use_proxy_get_data(proxy_addr,url):
        try:
            Req = urllib.request.Request(url)
            Req.add_header('user-agent',"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36")
            proxy = urllib.request.ProxyHandler({'http': proxy_addr})
            opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
            data = urllib.request.urlopen(Req).read()
            return data
        except urllib.error.URLError as e1:
            if hasattr(e1, 'code'):
                print(e1.code)
            if hasattr(e1, 'reason'):
                print(e1.reason)
            #产生异常则延时
            time.sleep(10)
        except Exception as e2:
            print("Exception:" + e2)
            #产生异常则延时
            time.sleep(1)

def crawler(proxy_addr,keyword,page):
    try:
        new_keyword = urllib.request.quote(keyword)
        count = 0
        for index in range(1,page+1):
            url = 'http://weixin.sogou.com/weixin?query='+new_keyword+'&_sug_type_=&s_from=input&_sug_=y&type=2&page=' + str(index) + '&ie=utf8&w=01019900&dr=1'
            data = use_proxy_get_data(proxy_addr,url).decode('utf-8','ignore')
            url_and_title_pattern = '<a target="_blank" href="(.*?)".*?data-share=.*?>(.*?)</a>'
            url_and_title = re.findall(url_and_title_pattern, data, re.S)
            if url_and_title == []:
                print("此页爬取失败")
                continue
            for couple in url_and_title:
                url = couple[0].replace("amp;",'')
                #提取并处理标题
                title = couple[1].replace("<em><!--red_beg-->"+keyword+"<!--red_end--></em>",keyword)
                cannot_be_name = ['/','\\','\"','?',':','*','<','>','|']
                new_title = title
                for element in cannot_be_name:
                    if element in title:
                        new_title = title.replace(element, ' ')
                print(title)
                #print(new_title)
                addr = 'D:/文件/学习/Python/网络爬虫/Wechat_articles/'+new_title+'.html'
                #file = open(addr,'wb')
                urllib.request.urlretrieve(url, filename=addr)
                #file.write(urllib.request.urlopen(url).read())
                print("第"+str(count+1)+"篇文章爬取成功！")
                count += 1
    except Exception as e2:
        print("Exception:" + e2)
        # 产生异常则延时
        time.sleep(1)
crawler('127.0.0.1:8888','Python',1)


