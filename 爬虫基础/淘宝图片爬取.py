#__author: ZhangWP
#date : 2018/8/7
import urllib.request
import re

opener = urllib.request.build_opener()
opener.add_handlers=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36')]
urllib.request.install_opener(opener)

def get_img_from_taobao(keyword,pages):
    keyword = urllib.request.quote(keyword)
    try:
        for i in range(0,pages):
            url = "https://s.taobao.com/search?q="+keyword+"&imgfile=&ie=utf8&bcoffset=0&ntoffset=0&s="+str(i*44)
            #print(url)
            data = urllib.request.urlopen(url).read().decode('utf-8','ignore')
            img_pattern = '"pic_url":"(.*?)"'
            img_urls = re.findall(img_pattern,data)
            for j in range(0,len(img_urls)):
                thisurl = 'http:' + img_urls[j]
                #print(thisurl)
                addr = 'D:/文件/学习/Python/网络爬虫/Taobao_Images/' + str(i) + str(j) + '.jpg'
                urllib.request.urlretrieve(thisurl,filename=addr)
                print("第"+str(i*44+j)+"幅图片爬取成功！")

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    except Exception as e2:
        print(e2)
def main():
    get_img_from_taobao('手机',1)

main()
