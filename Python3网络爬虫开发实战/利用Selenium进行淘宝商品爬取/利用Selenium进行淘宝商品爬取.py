from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymysql
import threading

Max_Page = 100

connection = pymysql.connect(user='root', password='Zwp0816...', host='127.0.0.1', db='taobaogoods')
cursor = connection.cursor()
cursor.execute('drop table if exists Goods;')
cursor.execute('create table Goods (名称 varchar(100), 价格 float, 成交量 varchar(100), 店铺 varchar(100), 地址 varchar(100));')
'''
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
'''
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
kw = '礼品'

global count
count = 0

def index_page(page):
    #print("==========================\n正在爬第"+str(page)+"页\n")
    try:
        url = 'https://s.taobao.com/search?q=' + quote(kw)
        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input'))
            )
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn'))
            )
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'),
                                             str(page))
        )
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.grid.g-clearfix .items .item'))
        )

        get_products()
    except TimeoutException:
        index_page(page)

def get_products():
    html = browser.page_source
    doc = pq(html)
    goods = doc('.item.J_MouserOnverReq').items()
    for item in goods:
        global count
        count += 1
        product = {
            #'image': item.find('.pic .img').attr('data-src'),
            'price': float(item.find('.price').text().replace('¥\n', '')),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop .shopname').text(),
            'location': item.find('.location').text(),
        }
        #print(product)
        save_to_mysql(product)
        print("第" + str(count) + "件商品写入完成")

def save_to_mysql(product):

    try:
        sql = 'insert into Goods values(%s, %s, %s, %s, %s)'
        cursor.execute(sql, (product['title'], product['price'], product['deal'], product['shop'], product['location']))
        connection.commit()
    except:
        connection.rollback()
    '''
    sql = 'insert into Goods values(%s, %s, %s, %s, %s)'
    cursor.execute(sql, (product['title'], product['price'], product['deal'], product['shop'], product['location']))
    connection.commit()
    '''

class Thread_A(threading.Thread):
    def __init__(self, start, lenth):
        threading.Thread.__init__(self)
        self.start = start
        self.lenth = lenth
    def run(self):
        for i in range(self.start, Max_Page+1, self.lenth):
            index_page(i)

class Thread_B(threading.Thread):
    def __init__(self, start, lenth):
        threading.Thread.__init__(self)
        self.start = start
        self.lenth = lenth
    def run(self):
        for i in range(self.start, Max_Page+1, self.lenth):
            index_page(i)

class Thread_C(threading.Thread):
    def __init__(self, start, lenth):
        threading.Thread.__init__(self)
        self.start = start
        self.lenth = lenth
    def run(self):
        for i in range(self.start, Max_Page+1, self.lenth):
            index_page(i)

class Thread_D(threading.Thread):
    def __init__(self, start, lenth):
        threading.Thread.__init__(self)
        self.start = start
        self.lenth = lenth
    def run(self):
        for i in range(self.start, Max_Page+1, self.lenth):
            index_page(i)

class Thread_E(threading.Thread):
    def __init__(self, start, lenth):
        threading.Thread.__init__(self)
        self.start = start
        self.lenth = lenth
    def run(self):
        for i in range(self.start, Max_Page+1, self.lenth):
            index_page(i)

def main():
    a = Thread_A(1, 5)
    a.run()
    b = Thread_B(2, 5)
    b.run()
    c = Thread_C(3, 5)
    c.run()
    d = Thread_D(4, 5)
    d.run()
    e = Thread_E(5, 5)
    e.run()
    connection.close()
    print("*****************\n全部写入完成！！")

if __name__ == '__main__':
    main()

