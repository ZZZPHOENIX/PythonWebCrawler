#__author: ZhangWP
#date : 2018/8/8

import re
import urllib.error
import urllib.request
import threading

opener = urllib.request.build_opener()
opener.addheaders=[('user-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36')]
urllib.request.install_opener(opener)

class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(1,36,2):
            try:
                url = 'https://www.qiushibaike.com/8hr/page/'+str(i*2)+'/'
                pagedata = urllib.request.urlopen(url).read().decode('utf-8')
                pat = '<div class="content">.*?<span>(.*?)</span>'
                datalist = re.findall(pat,pagedata,re.S)
                print(datalist)
                for j in range(0,len(datalist)):
                    print("第"+str(i)+"页第"+str(j)+"个段子的内容是：")
                    print(datalist[j])
            except urllib.error.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
            except Exception as e2:
                print(e2)

class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(2,35,2):
            try:
                url = 'https://www.qiushibaike.com/8hr/page/'+str(i*2)+'/'
                pagedata = urllib.request.urlopen(url).read().decode('utf-8')
                pat = '<div class="content">.*?<span>(.*?)</span>.*?</div>'
                datalist = re.findall(pat,pagedata,re.S)
                for j in range(0,len(datalist)):
                    print("第"+str(i)+"页第"+str(j)+"个段子的内容是：")
                    print(datalist[j])
            except urllib.error.URLError as e:
                if hasattr(e, "code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
            except Exception as e2:
                print(e2)

thread1=A()
thread2=B()
thread1.start()
thread2.start()
