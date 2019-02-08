import requests
from urllib.parse import quote
import re
import os
import jieba
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt


class getDelicacyInfo():
    def __init__(self, keyword):
        """
        初始化
        :param keyword:搜索关键词
        """
        self.restaurantIds = []
        self.keyword = keyword
        self.comments = {}

    def search(self):
        """
        搜索关键词
        :return: 商家链接列表
        """
        print("正在搜索相关信息...")

        mainUrl = "http://chs.meituan.com/s/" + quote(self.keyword) + '/'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': '__mta=19249927.1537181758802.1537331606782.1537345401430.10; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=165e72bf9c4c8-0a3c42315e4bad-74173c43-1fa400-165e72bf9c7c8; ci=70; rvct=70; uuid=7732b6b5aac643a8a0e4.1537331595.1.0.0; __mta=19249927.1537181758802.1537181758802.1537331596639.2; _lxsdk=165e72bf9c4c8-0a3c42315e4bad-74173c43-1fa400-165e72bf9c7c8; lat=28.189866; lng=112.974542; _lxsdk_s=165f0ed2c2d-37b-76b-aa7%7C%7C4',
            'Host': 'chs.meituan.com',
            'Referer': mainUrl,
            'Upgrade-Insecure-Requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36',
        }
        searchPage = requests.get(mainUrl, headers=headers).text
        self.restaurantIds = re.compile('<div class="list-item-desc-top"><a href="//www.meituan.com/meishi/(.*?)/"').findall(searchPage)

    def getComments(self, restaurantId):
        """
        获取商家评论信息
        :param restaurantId:商家ID号
        :return: 返回商家评论信息 [{count:出现次数, tag:评论关键字},]
        """
        commentUrl = "http://www.meituan.com/meishi/api/poi/getMerchantComment?"
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36',
            'Cookie': 'uuid=4206bb3f9f074b969c33.1537181736.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=165e72bf9c4c8-0a3c42315e4bad-74173c43-1fa400-165e72bf9c7c8; __mta=146519563.1537181747116.1537181747116.1537181747116.1; ci=70; rvct=70; _lxsdk=165e72bf9c4c8-0a3c42315e4bad-74173c43-1fa400-165e72bf9c7c8; client-id=fe47a6ca-19e9-44c0-889a-b6bc1b8db800; lat=28.19377; lng=112.9744; _lxsdk_s=165e7d98688-42d-287-a4d%7C%7C54',
            'Host': 'www.meituan.com',
            'Referer': commentUrl,
        }
        params = {
            'uuid': '4206bb3f9f074b969c33.1537181736.1.0.0',
            'platform': '1',
            'partner': '126',
            'originUrl': commentUrl,
            'riskLevel': '1',
            'optimusCode': '1',
            'id': restaurantId,
            'offset': 0,
            'pageSize': '10',
            'sortType': '1'
        }
        response = requests.get(commentUrl, params=params, headers=headers)
        pages = round((int(response.json()['data']['total']) + 5) / 10)
        i = 0
        self.comments[restaurantId] = []
        for page in range(pages):
            params['offset'] = page * 10
            self.comments[restaurantId] += self.parseComments(commentUrl, params, headers)
            print("第%s页评论处理完成" % (i+1))
            i += 1
        self.saveComments(restaurantId)

    def parseComments(self, commentUrl, params, headers):
        """
        提取页面评论信息
        :param commentUrl: 评论Ajax地址
        :param params: 请求参数
        :param headers: 请求头信息
        :return:
        """
        try:
            response = requests.get(commentUrl, params=params, headers=headers, timeout=2)
        except:
            self.parseComments(commentUrl, params, headers)

        comments = []
        try:
            for item in response.json()['data']['comments']:
                comments.append((item['comment'], int(item['star']/10)))
        except:
            pass
        return comments

    def saveComments(self, restaurantId):
        """
        保存评论文本信息至txt文档，生成并保存词云图片
        :param restaurantId:商家ID
        :return:
        """
        if len(self.comments[restaurantId]):
            if not os.path.exists('./MeituanCommets/'):
                os.mkdir('./MeituanCommets/')
            if not os.path.exists('./MeituanCommets/'+restaurantId+'/'):
                os.mkdir('./MeituanCommets/'+restaurantId+'/')
            with open('./MeituanCommets/'+restaurantId+'/comments.txt', 'w', encoding='utf-8') as f:
                score = 0
                for comment in self.comments[restaurantId]:
                    content = comment[0]
                    f.write(content+'\n')
                    score += comment[1]
                score = score / len(self.comments[restaurantId])
            self.drawWordCloud(restaurantId)

            print("评论保存成功，平均评价%.1f星" % score)

    def drawWordCloud(self, restaurantId):
        """
        生成并保存词云图片
        :param restaurantId: 商家ID
        :return:
        """
        print("正在绘制词云...\n")
        text = open('./MeituanCommets/'+restaurantId+'/comments.txt', encoding='utf-8').read()
        wordlist = ' '.join(jieba.cut(text))
        wordcloud = WordCloud(
            font_path='C:/Windows/Fonts/simhei.ttf',
            background_color='white',
            stopwords=STOPWORDS.add('味道'),
            width=2000,
            height=1720
            ).generate(wordlist)
        '''
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
        '''
        wordcloud.to_file('./MeituanCommets/'+restaurantId+'/wordCloud.png')

    def crawlRestaurants(self):
        """
        获取所有相关商家评论信息
        :return: 所有商家评论信息 {商家id:评论信息, }
        """
        self.search()
        counter = 0
        for id in self.restaurantIds:
            counter += 1
            if os.path.exists('./MeituanCommets/'+id+'/comments.txt'):
                continue
            print('-'*50 + "\n正在获取第%s个商家的评论信息...\n" % counter)
            self.getComments(id)

def main():
    crawler = getDelicacyInfo("臭豆腐")
    crawler.crawlRestaurants()

if __name__ == '__main__':
    main()