import requests
import re
import os

class getImage():
    def __init__(self, page):
        self.baseUrl = "http://thzu.net/"
        self.page = page
        self.seriesUrl = list()

        if not os.path.exists('./AdultImages/'):
            os.mkdir('./AdultImages/')

    def getPageContent(self, page):
        url = "http://thzu.net/forum-221-" + str(page) + ".html"
        src = requests.get(url).text
        urls = re.compile('<a href="(.*?)".*?class="z"').findall(src)
        return urls

    def getPages(self):
        seriesUrl = list()
        for i in range(self.page):
            seriesUrl += self.getPageContent(i)
        for i in range(len(seriesUrl)):
            seriesUrl[i] = self.baseUrl + seriesUrl[i]
        self.seriesUrl = seriesUrl

    def saveImage(self, url, no):
        pageContent = requests.get(url).text
        images = re.compile('class="zoom".*?file="(.*?)"').findall(pageContent)
        if not os.path.exists('./AdultImages/' + str(no) + '/'):
            os.mkdir('./AdultImages/' + str(no) + '/')
        count = 0
        for image in images:
            count += 1
            type = image.split('.')[-1]
            with open('./AdultImages/' + str(no) + '/' + str(count) + '.' + type, 'wb') as f:
                f.write(requests.get(image).content)

    def run(self):
        self.getPages()
        count = 0
        for series in self.seriesUrl:
            count += 1
            self.saveImage(series, count)

def main():
    crawler = getImage(1)
    crawler.run()

if __name__ == '__main__':
    main()