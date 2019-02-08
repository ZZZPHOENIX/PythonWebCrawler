#__author: ZhangWP
#date : 2018/8/7
import urllib.request
import urllib.parse

url = "http://www.iqianyue.com/mypost"

myPostData = urllib.parse.urlencode({"name":"Zwp","pass":"Password"}).encode('utf-8')

Req = urllib.request.Request(url,myPostData)
data = urllib.request.urlopen(Req).read()

file = open("test1.html",'wb')
file.write(data)
file.close()

