#__author: ZhangWP
#date : 2018/8/7
import urllib.request
import urllib.error
import re


opener = urllib.request.build_opener()
opener.add_handlers=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3486.0 Safari/537.36')]
urllib.request.install_opener(opener)

def get_img_from_Qiantu(pages):
    count = 0
    for i in range(0,pages):
        url = "http://www.58pic.com/tupian/huace-0-0-default-0-0-%E7%94%BB%E5%86%8C-0_1_0_0_0_0_1-"+str(i+1)+".html"
        #print(url)
        data = urllib.request.urlopen(url).read().decode('utf-8','ignore')
        img_pattern = '<img src="(http://.*?)\.jpg.*?"'
        img_urls = re.findall(img_pattern,data)
        #print(img_urls)
        try:
            for j in range(0,len(img_urls)):
                #print(img_urls[j])
                img_urls[j] += ".jpg"
                if img_urls[j] == "http://pic.58pic.com/images/everygg/5b077eba1575a.jpg":
                    continue
                addr = 'D:/文件/学习/Python/网络爬虫/Qiantu_Images/' + str(i) + str(j) + '.jpg'
                urllib.request.urlretrieve(img_urls[j],filename=addr)
                print("第"+str(count+1)+"幅图片爬取成功！")
                count += 1
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print(e.code)
            if hasattr(e,"reason"):
                print(e.reason)
        except Exception as e2:
            print(e2)

def main():
    get_img_from_Qiantu(5)

main()
