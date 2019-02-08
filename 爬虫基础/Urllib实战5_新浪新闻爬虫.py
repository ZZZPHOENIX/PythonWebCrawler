#__author: ZhangWP
#date : 2018/8/7
import urllib.request
import urllib.error
import re

start_url = "http://news.sina.com.cn/"

front_page = str(urllib.request.urlopen(start_url).read().decode('utf-8','ignore'))
pattern1 = '<a target="_blank" href="(.*?)"'
news_url = re.findall(pattern1,front_page)
'''
for element in news_url:
    print(element)
'''
print(len(news_url))

pattern2 = '<title>(.*?)</title>'
pattern3 = '<p>(.*?)</p>'
i = 0
for news in news_url:
    try:
        page = urllib.request.urlopen(news).read()
        title = re.findall(pattern2,page.decode('utf-8','ignore'))
        cannot_be_name = ['/', '\\', '\"', '?', ':', '*', '<', '>', '|']
        new_title = title[0]
        for element in cannot_be_name:
            if element in title[0]:
                new_title = title[0].replace(element, ' ')
        content = re.findall(pattern3, page.decode('utf-8', "ignore"))

        addr = 'D:/News/'+new_title+'.txt'
        print(addr)
        file = open(addr,'w',encoding='utf-8') #注意编码问题
        file.write(title[0]+'\n\n\n')
        for element in content:
            file.write(element+'\n')
        file.close()
        print("存储成功！")
        i+=1
    except urllib.error.URLError as error:
        if hasattr(error,"code"):
            print(error.code)
        if hasattr(error,"reason"):
            print(error.reason)
    except Exception as e:
        print(e)
        continue



