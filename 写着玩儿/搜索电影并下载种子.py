import requests
import re

class MovieHeaven():

    def __init__(self, target):
        """
        """
        self.searchUrl = "http://s.ygdy8.com/plus/so.php?"
        self.baseUrl = "http://www.ygdy8.com"
        self.keyword = target
        self.movieList = list()


    def searchMovie(self):
        """
        在搜索页面搜索电影，保存搜索结果至列表
        :return:
        """
        params = {
            'kwtype': 0,
            'keyword': self.keyword.encode('gb2312'),
        }
        page = requests.get(self.searchUrl, params=params)
        urls = re.compile("<td width='55%'><b><a href='(.*?)'").findall(page.text)
        if urls:
            for i in range(len(urls)):
                urls[i] = self.baseUrl + urls[i]
            self.movieList = urls
            return True
        else:
            return False

    def showMovie(self):
        for i in range(len(self.movieList)):
            content = requests.get(self.movieList[i]).content
            content = content.decode('gb2312', 'replace').encode('gbk', 'ignore')
            page = content.decode('gbk')
            info = re.compile('◎(.*?)<br').findall(page)[:10]
            print("序号：%s" % (i+1))
            for item in info:
                print(item)
            print('\n')

    def chooseMovie(self):
        index = int(input("输入选择的电影序号 >>>")) - 1
        content = requests.get(self.movieList[index]).content.decode('gb2312', 'replace').encode('gbk','ignore').decode('gbk')
        try:
            downloadUrl = re.compile('''<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(.*?)"''').findall(content)[0]
            print("下载地址：%s" % downloadUrl)
        except:
            print("未发现下载地址！请自行前往电影主页查看：%s" % self.movieList[index])





    def run(self):
        self.searchMovie()
        if self.movieList:
            print("搜索成功...")
            self.showMovie()
            self.chooseMovie()
        else:
            print("无搜索结果！")



def main():
    keyword = input("输入关键词 >>>")
    cralwer = MovieHeaven(keyword)
    cralwer.run()

if __name__ == '__main__':
    main()
