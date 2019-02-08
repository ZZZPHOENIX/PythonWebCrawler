#__author: ZhangWP
#date : 2018/8/7
import urllib.request

url = "http://blog.csdn.net/ZZPHOENIX/article/details/79492262"
header = ('user-agent',"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36")
opener = urllib.request.build_opener()
opener.add_handlers=[header]

data = opener.open(url).read()

file = open("test1.html",'wb')
file.write(data)
file.close()
print(data)