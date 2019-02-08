import requests
import re
import urllib.parse

class getMovie():
    def searchMovie(self):
        pass

    def getInfo(self, stack):
        pass

    def refresh(self):
        self.keyword = None
        self.movieUrlList = list()
        self.movieInfo = list()

    def run(self):
        if self.searchMovie():
            print("搜索成功...")
            self.getInfo()
        else:
            print("无搜索结果！")

class HD_Radio(getMovie):
    def __init__(self):
        self.searchUrl = "https://gaoqing.fm/s.php?"
        self.keyword = None
        self.movieUrlList = list()
        self.movieInfo = list()

    def searchMovie(self):
        print("START SEARCHING")
        params = {
            'q': self.keyword,
        }
        page = requests.get(self.searchUrl, params=params)
        print("Got Page Content")
        urls = re.compile('<a target="_blank" href="(.*?)"><h4 style="margin-top:0px;').findall(page.text)
        print("Got Urls")
        if urls:
            self.movieUrlList = urls
            print("SEARCH DONE")
            return True
        else:
            return False

    def getInfo(self, stack):
        for i in range(len(self.movieUrlList)):
            content = requests.get(self.movieUrlList[i]).content
            page = content.decode('utf8')

            info =list()
            name = re.compile('<a style="text-decoration:none;color:black;line-height:30px;" >(.*?)<').findall(page)[0]
            info.append(name)

            try:
                location = re.compile('地区</span>.*?>(.*?)</a').findall(page)[0]
            except Exception as e:
                location = None
            info.append(location)

            try:
                time = re.compile('上映</span>.*?>(.*?)</a').findall(page)[0]
            except Exception as e:
                time = None
            info.append(time)

            try:
                score = re.compile('评分</span>：<.*?>(.*?)</').findall(page)[0]
            except Exception as e:
                score = None
            info.append(score)

            downloadUrl = re.compile('''rel="nofollow" href="(.*?)" > 磁力''').findall(page)
            info.append(downloadUrl)

            temp = list(range(11))
            temp[1] = info[0]
            temp[2] = info[2]
            temp[3] = info[1]
            temp[7] = info[3]
            temp[9] = info[4]
            temp[10] = "高清电台"
            self.movieInfo.append(temp)
            stack.insert(-1, 1)

            print("Movie No.%s has been scratched." % i)
            print(info)

class MovieHeaven(getMovie):

    def __init__(self):
        self.searchUrl = "http://s.ygdy8.com/plus/so.php?"
        self.baseUrl = "http://www.ygdy8.com"
        self.keyword = None
        self.movieUrlList = list()
        self.movieInfo = list()

    def searchMovie(self):
        """
        在搜索页面搜索电影，保存搜索结果至列表
        :return:
        """
        print("START SEARCHING")
        params = {
            'typeid': 1,
            'keyword': self.keyword.encode('gb2312'),
        }
        page = requests.get(self.searchUrl, params=params)
        print("Got Page Content")
        urls = re.compile("<td width='55%'><b><a href='(.*?)'").findall(page.text)
        print("Got Urls")
        if urls:
            for i in range(len(urls)):
                urls[i] = self.baseUrl + urls[i]
            self.movieUrlList = urls
            print("SEARCH DONE")
            return True
        else:
            return False

    def getInfo(self, stack):
        for i in range(len(self.movieUrlList)):
            content = requests.get(self.movieUrlList[i]).content
            content = content.decode('gb2312', 'replace').encode('gbk', 'ignore')
            page = content.decode('gbk')

            info = re.compile('◎(.*?)<br').findall(page)[:10]
            downloadUrl = re.compile('''<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(.*?)"''').findall(page)[0]
            info.append(downloadUrl)

            temp = list(range(11))
            for j in range(len(info)):
                info[j] = info[j].replace("&nbsp;", "")
                info[j] = info[j].replace("&middot;", "")
                info[j] = info[j].replace("&orcirc;", "")
                if ("译　　名") in info[j]:
                    temp[0] = info[j].replace("译　　名", "").replace("　", '')
                if ("中 文 名") in info[j]:
                    temp[0] = info[j].replace("中 文 名", "").replace("　", '')
                elif ("英 文 名") in info[j]:
                    temp[1] = info[j].replace("英 文 名", "").replace("　", '')
                elif ("片　　名") in info[j]:
                    temp[1] = info[j].replace("片　　名", "").replace("　", '')
                elif ("年　　代") in info[j]:
                    temp[2] = info[j].replace("年　　代", "").replace("　", '')
                elif ("产　　地") in info[j]:
                    temp[3] = info[j].replace("产　　地", "").replace("　", '')
                elif ("国　　家") in info[j]:
                    temp[3] = info[j].replace("国　　家", "").replace("　", '')
                elif ("类　　别") in info[j]:
                    temp[4] = info[j].replace("类　　别", "").replace("　", '')
                elif ("语　　言") in info[j]:
                    temp[5] = info[j].replace("语　　言", "").replace("　", '')
                elif ("上映日期") in info[j]:
                    temp[6] = info[j].replace("上映日期", "").replace("　", '')
                elif ("IMDb评分") in info[j]:
                    temp[7] = info[j].replace("IMDb评分", "").replace("　", '')
                elif ("豆瓣评分") in info[j]:
                    temp[8] = info[j].replace("豆瓣评分", "").replace("　", '')
            temp[9] = [info[10]]
            temp[10] = "电影天堂"

            self.movieInfo.append(temp)
            stack.insert(-1, 1)

            print("Movie No.%s has been scratched." % i)


class BTzhijia(getMovie):

    def __init__(self):
        self.searchUrl = "https://www.btzhijia.com/s/"
        self.baseUrl = "https://www.btzhijia.com"
        self.keyword = None
        self.movieUrlList = list()
        self.movieInfo = list()

    def searchMovie(self):
        """
        在搜索页面搜索电影，保存搜索结果至列表
        :return:
        """
        print("START SEARCHING")
        url = self.searchUrl + urllib.parse.quote(self.keyword) + ".html"
        page = requests.get(url)
        print("Got Page Content")
        urls = re.compile('<a href="(.*?)" class="name" target="_blank">').findall(page.text)
        print("Got Urls")
        if urls:
            for i in range(len(urls)):
                urls[i] = self.baseUrl + urls[i]
            self.movieUrlList = urls
            print("SEARCH DONE")
            return True
        else:
            return False

    def getInfo(self, stack):
        for i in range(len(self.movieUrlList)):
            content = requests.get(self.movieUrlList[i]).content
            page = content.decode('utf8')

            info =list()
            name = re.compile('<meta property="og:title" content="(.*?)"').findall(page)[0]
            info.append(name)

            try:
                location = re.compile('地区：(.*?)&nbsp').findall(page)[0]
            except Exception as e:
                location = None
            info.append(location)

            try:
                time = re.compile('年份：(.*?)<').findall(page)[0]
            except Exception as e:
                time = None
            info.append(time)

            try:
                score = re.compile('''豆瓣(<span class='score'>(.*?)</span>)''').findall(page)[0]
            except Exception as e:
                score = None
            info.append(score)

            try:
                type = re.compile('<li>类型：.*?>(.*?)<').findall(page)[0]
            except Exception as e:
                type = None
            info.append(type)

            try:
                downloadPageUrl = re.compile('''li class='d_todo'>.*?href='(.*?.html)''', re.S).findall(page)[0]
                downloadPageUrl = self.baseUrl + downloadPageUrl
                urlPage = requests.get(downloadPageUrl).content.decode('utf8')

                downloadUrl = re.compile("""<a href='(.*?)' rel="nofollow" """).findall(urlPage)
                if len(downloadUrl) >= 2:
                    downloadUrl[1] = self.baseUrl + downloadUrl[1]
            except Exception as e:
                downloadUrl = None
            info.append(downloadUrl)

            temp = list(range(11))
            temp[1] = info[0]
            temp[2] = info[2]
            temp[3] = info[1]
            temp[4] = info[4]
            temp[8] = info[3]
            temp[9] = info[5]
            temp[10] = "BT之家"
            self.movieInfo.append(temp)
            stack.insert(-1, 1)

            print("Movie No.%s has been scratched." % i)
            print(info)

class HD_MP4(getMovie):

    def __init__(self):
        self.searchUrl = "http://www.98tvs.com"
        self.baseUrl = ""
        self.keyword = None
        self.movieUrlList = list()
        self.movieInfo = list()

    def searchMovie(self):
        print("START SEARCHING")

        page = requests.get(self.searchUrl, params={'s': self.keyword,})
        print("Got Page Content")
        urls = re.compile('<a href="(.*?)" class="zoom" rel="bookmark"').findall(page.text)
        print("Got Urls")
        if urls:
            self.movieUrlList = urls
            print("SEARCH DONE")
            return True
        else:
            return False

    def getInfo(self, stack):
        for i in range(len(self.movieUrlList)):
            content = requests.get(self.movieUrlList[i]).content
            page = content.decode('utf8')

            info =list()
            name = re.compile('<title>(.*?)<').findall(page)[0]
            info.append(name)

            try:
                downloadUrl = re.compile('<a rel="nofollow" href="(.*?)"').findall(page)
            except Exception as e:
                downloadUrl = None
            info.append(downloadUrl)

            temp = list(range(11))
            temp[1] = info[0]
            temp[9] = info[1]
            temp[10] = "高清MP4吧"
            self.movieInfo.append(temp)
            stack.insert(-1, 1)

            print("Movie No.%s has been scratched." % i)

class Chinese_HD(getMovie):
    def __init__(self):
        self.searchUrl = "http://gaoqing.la"
        self.keyword = None
        self.movieUrlList = list()
        self.movieInfo = list()

    def searchMovie(self):
        print("START SEARCHING")
        params = {
            's': self.keyword,
        }
        page = requests.get(self.searchUrl, params=params)
        print("Got Page Content")
        urls = re.compile('<a href="(.*?)" class="zoom" rel="bookmark"').findall(page.text)
        print("Got Urls")

        for i in range(len(urls)):
            if urls[i] == "http://gaoqing.la/questions":
                urls.pop(i)

        if len(urls) > 0:
            self.movieUrlList = urls
            print("SEARCH DONE")
            return True
        else:
            return False

    def getInfo(self, stack):
        for i in range(len(self.movieUrlList)):
            page = requests.get(self.movieUrlList[i]).text

            info = re.compile('◎(.*?)<').findall(page)[:10]

            temp = list(range(11))
            for j in range(len(info)):
                if ("译　　名") in info[j]:
                    temp[0] = info[j].replace("译　　名", "").replace("　", '')
                if ("中 文 名") in info[j]:
                    temp[0] = info[j].replace("中 文 名", "").replace("　", '')
                elif ("英 文 名") in info[j]:
                    temp[1] = info[j].replace("英 文 名", "").replace("　", '')
                elif ("片　　名") in info[j]:
                    temp[1] = info[j].replace("片　　名", "").replace("　", '')
                elif ("年　　代") in info[j]:
                    temp[2] = info[j].replace("年　　代", "").replace("　", '')
                elif ("产　　地") in info[j]:
                    temp[3] = info[j].replace("产　　地", "").replace("　", '')
                elif ("国　　家") in info[j]:
                    temp[3] = info[j].replace("国　　家", "").replace("　", '')
                elif ("类　　别") in info[j]:
                    temp[4] = info[j].replace("类　　别", "").replace("　", '')
                elif ("语　　言") in info[j]:
                    temp[5] = info[j].replace("语　　言", "").replace("　", '')
                elif ("上映日期") in info[j]:
                    temp[6] = info[j].replace("上映日期", "").replace("　", '')
                elif ("IMDb评分") in info[j]:
                    temp[7] = info[j].replace("IMDb评分", "").replace("　", '')
                elif ("豆瓣评分") in info[j]:
                    temp[8] = info[j].replace("豆瓣评分", "").replace("　", '')

            downloadUrl = re.compile('color: #ff0000;" href="(.*?)"').findall(page)
            if len(downloadUrl) > 0:
                temp[9] = downloadUrl
                temp[10] = "中国高清网"

                self.movieInfo.append(temp)
                stack.insert(-1, 1)
                print("Movie No.%s has been scratched." % i)


def main():
    keyword = input("输入关键词 >>>")
    cralwer = Chinese_HD()
    cralwer.keyword = keyword
    cralwer.run()

if __name__ == '__main__':
    main()
