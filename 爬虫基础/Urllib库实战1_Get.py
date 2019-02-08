import urllib.request

kw = "张蔚鹏"
kw = urllib.request.quote(kw)
url = "http://www.baidu.com/s?wd=" + kw +"&ie=utf-8&tn=baiduhome_pg"
Req = urllib.request.Request(url)
data = urllib.request.urlopen(Req).read()

file = open("test1.html",'wb')
file.write(data)
file.close()