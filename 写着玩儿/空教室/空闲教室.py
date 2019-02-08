import requests
import json
import tesserocr
import re
from PIL import Image
import os
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions
from selenium.common import exceptions
import datetime

class Crawler():
    def __init__(self):
        self.s = requests.session()
        self.browser = None

        self.cookies = None
        self.buildings = {
            'A座': '500137',
            'B座': '500138',
            'C座': '500139',
            'D座': '500140',
            '升华前楼': '500153',
            '科教南楼': '500154',
            '科教北楼': '500155',
        }

    def get_code(self):
        CAPCHAImage = self.browser.find_element_by_xpath('//*[@class="codeImg"]')
        left = CAPCHAImage.location['x']
        top = CAPCHAImage.location['y']
        right = left + CAPCHAImage.size['width']
        bottom = top + CAPCHAImage.size['height']
        self.browser.save_screenshot('screenshot.png')
        image = Image.open('screenshot.png').crop((left, top, right, bottom))
        image = image.convert('RGB')

        #图像预处理
        image = image.convert('L')
        threshold = 200
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, '1')
        #image.show()

        code = str(tesserocr.image_to_text(image)).replace(' ', '')

        #处理code长度不等于4的情况
        if len(code) < 4:
            code = '0000'
        code = code[:4]

        return code

    def login_selenium(self):
        print("正在登陆...")

        opt = ChromeOptions()
        opt.add_argument('--headless')
        #self.browser = Chrome(chrome_options=opt)
        self.browser = Chrome()

        self.browser.get('http://classroom.csu.edu.cn')
        wait = WebDriverWait(self.browser, 5)
        inputAccount = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_easyui_textbox_input1"]')))
        inputPassword = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_easyui_textbox_input2"]')))
        inputCAPCHA = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_easyui_textbox_input3"]')))
        loginBtn = self.browser.find_element_by_xpath('//*[@id="btn_login"]')

        inputAccount.send_keys('0902170117')
        inputPassword.send_keys('199908')
        inputCAPCHA.send_keys(self.get_code())
        loginBtn.click()
        retry_counting = 0
        while True:
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="自习教室"]')))
                break
            except exceptions.TimeoutException:
                print("登录失败，重试...")
                retry_counting += 1
                if retry_counting > 5:
                    self.login_selenium()
                try:
                    alert_ok_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="alert_ok_btn"]')))
                    alert_ok_btn.click()
                    inputCAPCHA.send_keys(self.get_code())
                    loginBtn.click()
                except exceptions.TimeoutException:
                    self.login_selenium()


        self.cookies = self.browser.get_cookies()
        self.browser.close()
        for i in self.cookies:
            requests.utils.add_dict_to_cookiejar(self.s.cookies, {i['name']: i['value']})

        print("登陆成功...")
        os.remove('screenshot.png')

    def login(self):
        main_url = 'http://classroom.csu.edu.cn'
        response = self.s.get(main_url)
        time_stamp = re.compile('data-timestamp="(.*?)"').findall(response.text)[0]

        logincode_url = 'http://classroom.csu.edu.cn/logincode.do'
        params = {'t1': time_stamp}
        image_content = self.s.get(logincode_url, params=params).content

        with open('C:/Users/ZhangWP/Desktop/code.jpg', 'wb') as img:
            img.write(image_content)
        image = Image.open('C:/Users/ZhangWP/Desktop/code.jpg')
        code = tesserocr.image_to_text(image)
        print(code)
        login_url = 'http://classroom.csu.edu.cn/sys/login.do?aa=123'
        data = {
            'userName': '0902170117',
            'password': '199908',
            'code': code,
        }
        content = self.s.post(login_url, data=data)

        print(response.text)
        os.remove('C:/Users/ZhangWP/Desktop/code.jpg')
        return content

    def choose(self):
        print("选择教学楼：")
        for i in range(len(list(self.buildings.keys()))):
            print("序号：%s 教学楼：%s" % (i+1, list(self.buildings.keys())[i]))
        building = list(self.buildings.keys())[int(input('  >>>'))-1]
        month = input("月份：")
        day = input("日：")
        date = "2018-" + month + "-" + day

        return (building, date)

    def get_source(self, info):
        url = 'http://classroom.csu.edu.cn/common/leisureBuildingRoom.do'
        building = info[0]
        date = info[1]

        data = {
            'buildBh': self.buildings[building],
            'sj': date,
        }
        content = self.s.post(url, data=data).text
        with open('%s-%s.json' % (building, date), 'w') as f:
            f.write(content)
        #print(content)
        return content

    def parse_source(self, source):
        periods = {
            '1': '8:00~9:40',
            '2': '10:00~11:40',
            '3': '14:00~15:40',
            '4': '16:00~17:40',
            '5': '19:00~20:40',
        }

        leisure_room = {
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [],
        }

        a = json.loads(source)

        for i in a['obj']['roomlist']:
            for period in i['record']:
                if 1 <= period['room_period'] <= 5 and period['room_state'] == '0':
                    leisure_room[str(period['room_period'])].append(i['room_name'])

        for item in leisure_room:
            print(periods[item], end='\t')
            for period in leisure_room[item]:
                print(period, end='\t')
            print('')

    def search(self):
        choice = self.choose()
        if not os.path.exists('%s-%s.json' % (choice[0], choice[1])):
            self.login_selenium()
            source = self.get_source(choice)
        else:
            with open('%s-%s.json' % (choice[0], choice[1])) as f:
                source = f.read()
        self.parse_source(source)

    def download_all_info(self):
        self.login_selenium()

        time = []
        now = datetime.datetime.now()
        time.append(now.strftime('%Y-%m-%d'))
        for i in range(1, 7):
            time.append((now + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
        for building in self.buildings:
            for date in time:
                print("正在爬取%s %s的空闲教室信息..." % (building, date))
                self.get_source((building, date))

        print("全部爬取完成！！")

def main():
    spyder = Crawler()
    #spyder.download_all_info()
    spyder.search()

if __name__ == '__main__':
    main()
