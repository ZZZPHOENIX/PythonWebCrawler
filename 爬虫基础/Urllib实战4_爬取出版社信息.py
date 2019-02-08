#__author: ZhangWP
#date : 2018/8/7
import re
import urllib.request

url = "https://read.douban.com/provider/all"
data = urllib.request.urlopen(url).read()
data = data.decode("UTF-8")

pattern1 = '<div class="name">(.*?)</div>'
result = re.findall(pattern1,data)
#print(len(result))

file = open('D:\\test.txt','w')
for element in result:
    file.write(element+'\n')
file.close()

