from selenium import webdriver
#from selenium.webdriver.support
from PIL import Image
import time
from io import BytesIO
import colorsys
import pymysql

class AutoStudent():
    def __init__(self):

        self.courseList = list()

        self.db = pymysql.connect(host='127.0.0.1', user='root', password='***', db='ChaoXingStuInfo')
        self.cursor = self.db.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS StudentInfo(账号 VARCHAR(30), 密码 VARCHAR(20));')
        self.db.commit()

        # opt = webdriver.ChromeOptions()
        # opt.add_argument('--headless')
        # self.browser = webdriver.Chrome(chrome_options=opt)
        self.browser = None

    def login(self):
        choice1 = ''
        while True:
            self.cursor.execute('SELECT * FROM StudentInfo')
            result = self.cursor.fetchall()
            if result:
                print("\n===================数据库中已有学生信息===================")
                for i in range(0, len(result)):
                    print(
                        "\n编号：" + str(i + 1) + "\t账号：" + result[i][0] + '\t密码：' + result[i][1])
                print('\n')
                choice1 = input("是否使用数据库中已有学生信息？(y/n) >>>")
                if choice1 == 'y':
                    index = int(input("输入要使用的信息编号：")) - 1
                    try:
                        account = result[index][0]
                        password = result[index][1]
                        break
                    except:
                        print("输入错误！")
                        continue
                else:
                    account = input("输入账号：")
                    password = input("输入密码：")
                    break
            else:
                account = input("输入账号：")
                password = input("输入密码：")
                break
        if choice1 != 'y':
            choice2 = input("\n是否将学生信息存入数据库？(y/n)")
            if choice2 == 'y':
                if choice1 != 'y':
                    sql = 'INSERT INTO StudentInfo VALUES(%s, %s)'
                    self.cursor.execute(sql, (account, password))
                self.db.commit()

        print("\n正在登陆...")
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()

        loginUrl = "http://passport2.chaoxing.com/login?fid=185"
        self.browser.get(loginUrl)
        #定位元素位置
        inputAccount = self.browser.find_element_by_xpath('//*[@id="unameId"]')
        inputPassword = self.browser.find_element_by_xpath('//*[@id="passwordId"]')
        inputCAPCHA = self.browser.find_element_by_xpath('//*[@id="numcode"]')
        loginBtn = self.browser.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[7]/td[2]/label/input')
        '''
        验证码截图
        CAPCHAImage = re.compile('img src="(.*?)".*?id="numVerCode"').findall(self.browser.page_source)[0]
        CAPCHAImage = self.browser.find_element_by_xpath('//img[@id="numVerCode"]')
        left = CAPCHAImage.location['x']
        top = CAPCHAImage.location['y']
        right = left + CAPCHAImage.size['width']
        bottom = top + CAPCHAImage.size['height']
        image = image.crop((left, top, right, bottom))
        '''
        #填入信息
        inputAccount.send_keys(account)
        inputPassword.send_keys(password)
        #Image.open('./CAPCHAImage.jpg').show()
        self.browser.save_screenshot('screenshot.png')
        Image.open('screenshot.png').show()
        CAPCHA = input("输入验证码 >>>")
        inputCAPCHA.send_keys(CAPCHA)
        loginBtn.click()
        while self.browser.current_url == "http://passport2.chaoxing.com/login?refer=http%3A%2F%2Fi.mooc.chaoxing.com":
            print("登陆出错，请重新登陆...")
            self.login()
        print("登陆成功")

    def chooseCourse(self):
        #print(self.browser.page_source)
        #time.sleep(5)
        self.browser.switch_to.frame('frame_content')
        img = self.browser.find_element_by_xpath('//div[@class="Mcon1img httpsClass"]/a[1]')
        img.click()
        self.browser.switch_to.window(self.browser.window_handles[1])
        print("已进入课程界面")

    def getNextCourse(self):
        classes = self.browser.find_elements_by_css_selector('h3.clearfix')
        count = 0
        for i in range(len(classes)):
            if "orange" in classes[i].find_element_by_css_selector('.icon em').get_attribute('class'):
                if "综合测试题" not in classes[i].find_element_by_css_selector('.articlename').text:
                    course = classes[i].find_element_by_css_selector('.articlename')
                    count += 1
                    return course
        if count == 0:
            return False

    def watchVideo(self):
        course = self.getNextCourse()
        if not course:
            return False
        course.click()
        self.browser.switch_to.frame('iframe')
        #self.browser.switch_to.frame('ans-attach-online ans-insertvideo-online')
        playBtn = self.browser.find_element_by_css_selector('.ans-attach-ct')
        webdriver.ActionChains(self.browser).move_to_element(playBtn).perform()
        playBtn.click()
        while True:
            time.sleep(5)
            if self.ifFinished():
               break
        self.browser.back()
        self.browser.refresh()
        return True

    def ifFinished(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        screenshot.convert('RGB')
        target = self.browser.find_element_by_css_selector('div.ans-job-icon')
        left = 456
        top = 340
        elementWidth = left + target.size['width']
        elementHeight = top + target.size['height']

        screenshot = screenshot.crop((left, top, elementWidth, elementHeight))
        #screenshot.show()
        result = self.getDominantColor(screenshot)
        if 230<result[0]<245 and 165<result[1]<180 and 30<result[2]<45:
            print("Watching...")
            return False
        else:
            return True

    def getDominantColor(self, image):
        max_score = 0.0001
        dominant_color = None
        for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
            # 转为HSV标准
            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
            y = (y - 16.0) / (235 - 16)

            # 忽略高亮色
            if y > 0.9:
                continue
            score = (saturation + 0.1) * count
            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)
        return dominant_color

    def run(self):
        self.login()
        self.chooseCourse()
        while True:
            result = self.watchVideo()
            if not result:
                print("课程全部听取完成！")
                break

def main():
    robot = AutoStudent()
    robot.run()

if __name__ == '__main__':
    main()

