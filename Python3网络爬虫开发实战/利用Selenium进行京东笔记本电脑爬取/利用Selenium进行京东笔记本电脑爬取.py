from selenium import webdriver
import requests
from pyquery import PyQuery as pq
import pymysql
import re
import urllib.request

connection = pymysql.connect(user='root', password='***', host='127.0.0.1', db='JD_Goods')
cursor = connection.cursor()
#cursor.execute('drop table if exists pcinfo;')
#cursor.execute('create table pcinfo(名称 varchar(100), 价格 float, 评论 int, 内存 varchar(100), CPU类型 varchar(100), CPU型号 varchar(100), CPU速度 varchar(100), CPU核心 varchar(100), 硬盘容量 varchar(100), 固态硬盘 varchar(100), 显卡类型 varchar(100), 显示芯片 varchar(100), 显存容量 varchar(100), 尺寸 varchar(100), 重量 varchar(100), 链接 varchar(100));')
#cursor.execute('create table pcinfo(名称 varchar(100), 价格 varchar(100), 好评数 int, 差评数 int, 好评度 varchar(10), 内存 varchar(100), CPU类型 varchar(100), CPU型号 varchar(100), CPU速度 varchar(100), CPU核心 varchar(100), 硬盘容量 varchar(100), 固态硬盘 varchar(100), 显卡类型 varchar(100), 显示芯片 varchar(100), 显存容量 varchar(100), 尺寸 varchar(100), 重量 varchar(100), 链接 varchar(100));')
connection.commit()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')


# TOTAL为总页数
url = 'http://list.jd.com/list.html?cat=670,671,672&page=1'
TOTAL = int(re.findall('<em>共<b>(.*?)</b>', urllib.request.urlopen(url).read().decode('utf-8', 'ignore'))[0])
#TOTAL = 1

#start：起始页  end：终止页+1
start = 900
TOTAL = TOTAL - start + 1
end = start + TOTAL

global count, links, prices, comments, retry_index, retry_products, fail_links
count = 0
links = []
prices = []
comments = []
retry_index = []
retry_products = []
fail_links = []

def get_proxy():
    PROXY_POOL_URL = 'http://localhost:5555/random'
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

def get_url_price_and_comment(index):
    try:
        url = "http://list.jd.com/list.html?cat=670,671,672&page=" + str(index) + "&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main"
        page = urllib.request.urlopen(url).read().decode('gbk', 'ignore')

        global links, prices, comments
        results = re.compile('<a target="_blank" title="" href="(.*?)">').findall(page)
        for i in range(0, len(results)):
            results[i] = 'https:' + results[i]
        links += results
        '''
        while True:
            proxy = get_proxy()
            if proxy != None:
                break
        '''
        #chrome_options.add_argument('--proxy-server=http://' + proxy)
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.implicitly_wait(10)
        browser.get(url)

        html = browser.page_source
        doc = pq(html)
        browser.close()
        info = doc('.gl-item').items()
        for item in info:
            try:
                price = item.find('.J_price.js_ys').text()
                #print(price)
                price = float(price.replace('¥\n', ''))
            except:
                price = "NULL"
            prices.append(price)

            comment = item.find('.p-commit').text()
            comment = re.compile(r'已有\n(.*?)\n人评价').findall(comment)[0]
            #print(comment)
            if '万' in comment:
                comment = comment.replace('万+', '')
                comment = int(float(comment) * 10000)
            elif '+' in comment:
                comment = int(comment.replace('+', ''))
            comments.append(comment)
        #print("\n===============第" + str(index) + "页======代理ip:", proxy, "================\n")
        print("\n======================第" + str(index) + "页======================\n")

    except Exception as e:
        print(e)
        global retry_index
        retry_index.append(index)

def parse_with_price(page, link, price, comment):
    try:
        html = urllib.request.urlopen(link, timeout=5).read().decode('gbk', 'ignore')
        name = re.compile('<img id="spec-img".*?alt="(.*?)"', re.S).findall(html)[0]
        name = name.strip()

        result1 = re.compile('<dt>内存容量</dt>.*?<dd>(.*?)<', re.S).findall(html)
        result2 = re.compile('<dt>内存类型</dt>.*?<dd>(.*?)<', re.S).findall(html)
        result1 = result1[0] if result1 != [] else ''
        result2 = result2[0] if result2 != [] else ''
        internalStorage = result1 + result2
        # print(internalStorage)

        result = re.compile('<dt>CPU类型</dt>.*?<dd>(.*?)<', re.S).findall(html)
        cpu_type = result[0] if result != [] else ''
        # print(cpu_type)

        result = re.compile('<dt>CPU型号</dt>.*?<dd>(.*?)<', re.S).findall(html)
        cpu_Mode = result[0] if result != [] else ''
        # print(cpu_Mode)

        result = re.compile('<dt>CPU速度</dt>.*?<dd>(.*?)<', re.S).findall(html)
        cpu_speed = result[0] if result != [] else ''

        result = re.compile('<dt>核心</dt>.*?<dd>(.*?)<', re.S).findall(html)
        cpu_core = result[0] if result != [] else ''

        result = re.compile('<dt>硬盘容量</dt>.*?<dd>(.*?)<', re.S).findall(html)
        diskCapacity = result[0] if result != [] else ''

        result = re.compile('<dt>固态硬盘</dt>.*?<dd>(.*?)<', re.S).findall(html)
        SSD = result[0] if result != [] else ''

        result = re.compile('<dt>类型</dt>.*?<dd>(.*?)<', re.S).findall(html)
        GCtype = result[0] if result != [] else ''

        result = re.compile('<dt>显示芯片</dt>.*?<dd>(.*?)<', re.S).findall(html)
        GCcore = result[0] if result != [] else ''

        result = re.compile('<dt>显存容量</dt>.*?<dd>(.*?)<', re.S).findall(html)
        GCcapacity = result[0] if result != [] else ''

        result = re.compile('<dt>尺寸</dt>.*?<dd>(.*?)<', re.S).findall(html)
        size = result[0] if result != [] else ''

        result = re.compile('<dt>净重</dt>.*?<dd>(.*?)<', re.S).findall(html)
        weight = result[0] if result != [] else ''

        if price != 'NULL':

            sql = 'insert into pcinfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (
                name, price, comment, internalStorage, cpu_type, cpu_Mode, cpu_speed, cpu_core, diskCapacity, SSD,
                GCtype,
                GCcore, GCcapacity, size, weight, link))
            connection.commit()

            global count
            count += 1
            print("第" + str(page) + "页\t\t总第" + str(count) + "个商品处理完成\t\t完成度：" + str(
                int((count / (TOTAL * 60)) * 1000000) / 10000) + "%")

        else:
            global retry_products
            info = {'link': link, 'comment': comment}
            retry_products.append(info)
            print('! ! ! ! ! !错误: 价格为空\t稍后重试')

    except:
        '''
        处理“全球购”商品
        '''
        try:
            # 处理“全球购”商品

            html = urllib.request.urlopen(link, timeout=None).read().decode('gbk', 'ignore')
            name = re.compile("<img class='img-hover' alt='(.*?)'", re.S).findall(html)[0]
            name = name.strip()

            result1 = re.compile('<td class="tdTitle">最大支持容量.*?<td>(.*?)<', re.S).findall(html)
            result2 = re.compile('<td class="tdTitle">内存类型.*?<td>(.*?)<', re.S).findall(html)
            result1 = "最大支持容量" + result1[0] if result1 != [] else ''
            result2 = result2[0] if result2 != [] else ''
            internalStorage = result2 + ' ' + result1
            # print(internalStorage)

            result = re.compile('<td class="tdTitle">CPU类型</td>.*?<td>(.*?)<', re.S).findall(html)
            cpu_type = result[0] if result != [] else ''
            # print(cpu_type)

            result = re.compile('<tr><td class="tdTitle">CPU型号</td>.*?<td>(.*?)<', re.S).findall(html)
            cpu_Mode = result[0] if result != [] else ''
            # print(cpu_Mode)

            result = re.compile('<tr><td class="tdTitle">CPU速度</td>.*?<td>(.*?)<', re.S).findall(html)
            cpu_speed = result[0] if result != [] else ''

            result = re.compile('<td class="tdTitle">核心</td>.*?<td>(.*?)<', re.S).findall(html)
            cpu_core = result[0] if result != [] else ''

            result = re.compile('<td class="tdTitle">硬盘容量</td>.*?<td>(.*?)<', re.S).findall(html)
            diskCapacity = result[0] if result != [] else ''

            result = re.compile('<td class="tdTitle">固态硬盘</td>.*?<td>(.*?)<', re.S).findall(html)
            SSD = result[0] if result != [] else ''

            result = re.compile('<td class="tdTitle">类型</td>.*?<td>(.*?)<', re.S).findall(html)
            GCtype = result[0] if result != [] else ''

            result = re.compile('<td class="tdTitle">显示芯片</td>.*?<td>(.*?)<', re.S).findall(html)
            GCcore = result[0] if result != [] else ''

            result = re.compile('<td class="tdTitle">显存容量</td>.*?<td>(.*?)<', re.S).findall(html)
            GCcapacity = result[0] if result != [] else ''

            result = re.compile('<td class="tdTitle">屏幕尺寸</td>.*?<td>(.*?)<', re.S).findall(html)
            size = result[0] if result != [] else ''

            result = re.compile('<td class="tdTitle">净重</td>.*?<td>(.*?)<', re.S).findall(html)
            weight = result[0] if result != [] else ''

            sql = 'insert into pcinfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (
                name, price, comment, internalStorage, cpu_type, cpu_Mode, cpu_speed, cpu_core, diskCapacity, SSD,
                GCtype,
                GCcore, GCcapacity, size, weight, link))

            connection.commit()
            count += 1
            print("第" + str(page) + "页\t\t总第" + str(count) + "个商品处理完成\t\t完成度：" + str(
                int((count / (TOTAL * 60)) * 10000) / 100) + "%")
        except Exception as e:
            print("! ! ! ! ! !错误：", e, "\t稍后重试")
            info = {'link': link, 'comment': comment}
            retry_products.append(info)

def parse_without_price(page, link, comment):
    try:
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(link)
        doc = pq(browser.page_source)
        price = doc.find('.p-price .price').text()
        price = float(price)

        html = urllib.request.urlopen(link, timeout=None).read().decode('gbk', 'ignore')
        name = re.compile('<img id="spec-img".*?alt="(.*?)"', re.S).findall(html)[0]
        name = name.strip()

        result1 = re.compile('<dt>内存容量</dt>.*?<dd>(.*?)<', re.S).findall(html)
        result2 = re.compile('<dt>内存类型</dt>.*?<dd>(.*?)<', re.S).findall(html)
        result1 = result1[0] if result1 != [] else ''
        result2 = result2[0] if result2 != [] else ''
        internalStorage = result1 + result2
        # print(internalStorage)

        result = re.compile('<dt>CPU类型</dt>.*?<dd>(.*?)<', re.S).findall(html)
        cpu_type = result[0] if result != [] else ''
        # print(cpu_type)

        result = re.compile('<dt>CPU型号</dt>.*?<dd>(.*?)<', re.S).findall(html)
        cpu_Mode = result[0] if result != [] else ''
        # print(cpu_Mode)

        result = re.compile('<dt>CPU速度</dt>.*?<dd>(.*?)<', re.S).findall(html)
        cpu_speed = result[0] if result != [] else ''

        result = re.compile('<dt>核心</dt>.*?<dd>(.*?)<', re.S).findall(html)
        cpu_core = result[0] if result != [] else ''

        result = re.compile('<dt>硬盘容量</dt>.*?<dd>(.*?)<', re.S).findall(html)
        diskCapacity = result[0] if result != [] else ''

        result = re.compile('<dt>固态硬盘</dt>.*?<dd>(.*?)<', re.S).findall(html)
        SSD = result[0] if result != [] else ''

        result = re.compile('<dt>类型</dt>.*?<dd>(.*?)<', re.S).findall(html)
        GCtype = result[0] if result != [] else ''

        result = re.compile('<dt>显示芯片</dt>.*?<dd>(.*?)<', re.S).findall(html)
        GCcore = result[0] if result != [] else ''

        result = re.compile('<dt>显存容量</dt>.*?<dd>(.*?)<', re.S).findall(html)
        GCcapacity = result[0] if result != [] else ''

        result = re.compile('<dt>尺寸</dt>.*?<dd>(.*?)<', re.S).findall(html)
        size = result[0] if result != [] else ''

        result = re.compile('<dt>净重</dt>.*?<dd>(.*?)<', re.S).findall(html)
        weight = result[0] if result != [] else ''

        if price != 'NULL':

            sql = 'insert into pcinfo values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (
                name, price, comment, internalStorage, cpu_type, cpu_Mode, cpu_speed, cpu_core, diskCapacity, SSD,
                GCtype,
                GCcore, GCcapacity, size, weight, link))
            connection.commit()
            global count
            count += 1
            print("第" + str(page) + "页\t\t总第" + str(count) + "个商品处理完成\t\t完成度：" + str(
                int((count / (TOTAL * 60)) * 1000000) / 10000) + "%")

        else:
            global retry_products
            info = {'link': link, 'comment': comment}
            retry_products.append(info)
            print('! ! ! ! ! !错误: 价格为空\t稍后重试')

    except Exception as e:
        print("* * * * * 商品信息无法处理，错误原因：", e, "\t链接：", link)
        global fail_links
        fail_links.append(link)

def get_product(page):
    global links, prices, comments
    link = links.pop(0)
    price = prices.pop(0)
    comment = comments.pop(0)
    parse_with_price(page, link, price, comment)

def retry_product(page):
    global retry_products
    info = retry_products.pop(0)
    link = info['link']
    comment = info['comment']

    parse_without_price(page, link, comment)



def main():
    print("\n开始处理商品...")

    for i in range(start, end):
        get_url_price_and_comment(i)

        while links != []:
            try:
                get_product(i)
            except:
                pass

        if retry_products!=[]:
            print("\t--------正在重新处理错误商品--------")
            while retry_products != []:
                try:
                    retry_product(i)
                except:
                    pass
        print("\n第" + str(i) + "页处理完成")

    while retry_index!=[]:
        index = retry_index.pop(0)
        get_url_price_and_comment(index)
        if retry_products!=[]:
            print("\t--------正在重新处理错误商品--------")
            while retry_products != []:
                retry_product(i)
        print("\n第" + str(index) + "页处理完成")

    print("**************所有商品链接处理完成**************")

    if fail_links!=[]:
        print("\n以下商品无法处理：")
        for link in fail_links:
            print('\t'+link)



if __name__ == '__main__':
    main()

