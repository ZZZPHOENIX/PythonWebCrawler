import requests
from urllib.parse import urlencode
import pymysql
import sched
import re
import datetime
import time
import smtplib
import email.mime.multipart
import email.mime.text
from multiprocessing import Pool
import warnings

warnings.filterwarnings("ignore")


class Book_Ticket():

    def connect_database(self):
        self.db = pymysql.connect(host='localhost', user='root', password='Zwp0816...', db='Qunar')
        self.cursor = self.db.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS PassengerInfo(乘客姓名 VARCHAR(50), 乘客身份证号 VARCHAR(100));')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ContactInfo(联系人姓名 VARCHAR(50), 联系人电话 VARCHAR(20));')
        self.db.commit()

    def get_info_passenger(self):
        while True:
            self.cursor.execute('SELECT * FROM PassengerInfo')
            result = self.cursor.fetchall()
            if result:
                print("\n===================数据库中已有乘客信息===================")
                for i in range(0, len(result)):
                    print(
                        "\n编号：" + str(i + 1) + "\t乘客姓名：" + result[i][0] + '\t乘客身份证号：' + result[i][1])
                print('\n')
                choice1 = input("是否使用数据库中已有乘客信息？(y/n) >>>")
                if choice1 == 'y':
                    index = int(input("输入要使用的信息编号：")) - 1
                    try:
                        self.pName = result[index][0]
                        self.pIdNo = result[index][1]
                    except:
                        print("输入错误！")
                        continue
                else:

                    self.pName = input("输入乘客姓名：")
                    self.pIdNo = input("输入乘客身份证号：")
            else:
                self.pName = input("输入乘客姓名：")
                self.pIdNo = input("输入乘客身份证号：")

            self.cursor.execute('SELECT * FROM ContactInfo')
            result = self.cursor.fetchall()
            if result:
                print("\n===================数据库中已有联系人信息===================")

                for i in range(0, len(result)):
                    print("\n编号：" + str(i + 1) + '\t联系人姓名：' + result[i][0] + '\t联系人电话：' + result[i][1])
                print('\n')
                choice2 = input("是否使用数据库中已有联系人信息？(y/n) >>>")
                if choice2 == 'y':
                    index = int(input("输入要使用的信息编号：")) - 1
                    try:
                        self.cName = result[index][0]
                        self.cPhone = result[index][1]
                    except:
                        print("输入错误！")
                        continue
                else:
                    self.cName = input("输入联系人姓名：")
                    self.cPhone = input("输入联系人电话：")

            else:
                self.cName = input("输入联系人姓名：")
                self.cPhone = input("输入联系人电话：")

            self.From = input("\n输入出发城市：")
            self.To = input("输入目的地城市：")
            self.Date = input("输入出发日期(格式为2018-01-01)：")
            self.pInsureNo = input("是否购买￥30的保险(y/n)：")
            print("\n输入的信息如下：")
            print("\n出发城市：", self.From)
            print("目的地城市：", self.To)
            print("出发日期：", self.Date)
            print("乘客姓名：", self.pName)
            print("乘客身份证号：", self.pIdNo)
            print("联系人姓名：", self.cName)
            print("联系人电话：", self.cPhone)
            print("是否购买保险：", self.pInsureNo)
            choice = input("\n确认信息无误？(y/n) >>>")
            if choice == 'y':
                if choice1 != 'y' or choice2 != 'y':
                    choice3 = input("\n是否将乘客、联系人信息存入数据库？(y/n)")
                    if choice3 == 'y':
                        if choice1 != 'y':
                            sql = 'INSERT INTO PassengerInfo VALUES(%s, %s)'
                            self.cursor.execute(sql, (self.pName, self.pIdNo))
                        if choice2 != 'y':
                            sql = 'INSERT INTO ContactInfo VALUES(%s, %s)'
                            self.cursor.execute(sql, (self.cName, self.cPhone))
                        self.db.commit()

                if len(self.pIdNo) == 15:
                    self.pGender = 1 if int(self.pIdNo[14]) % 2 == 1 else 2
                    self.pBirthday = '19' + self.pIdNo[6:12]
                    self.pInsureNo = '1002103,YD' if self.pInsureNo == 'y' else '-1'
                    break
                elif len(self.pIdNo) == 18:
                    self.pGender = 1 if int(self.pIdNo[16]) % 2 == 1 else 2
                    self.pBirthday = self.pIdNo[6:14]
                    self.pInsureNo = '1002103,YD' if self.pInsureNo == 'y' else '-1'
                    break
                else:
                    print("\n信息错误！")
            else:
                print("\n重新输入！")

    def get_info_single_way(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36'
        }
        params = {
            'dptStation': self.From,
            'arrStation': self.To,
            'date': self.Date,
            'type': 'normal',
            'user': 'neibu',
            'source': 'site',
            'start': 1,
            'num': 500,
            'sort': 3,
        }
        url = 'https://train.qunar.com/dict/open/s2s.do?'
        try:
            response = requests.get(url, params=params, headers=headers, verify=False)
            self.data = response.json()['data']['s2sBeanList']
        except Exception as  e:
            print(e)
            print("\n* * * 日期信息错误！* * *")

    def parse_and_show_data(self):
        try:
            if not self.data:
                print('* * * 无相关车次信息')
                exit()
        except:
            print('* * * 无相关车次信息 * * *')
            exit()

        self.DATA = []
        for item in self.data:
            # 终点信息
            arrStation = item['arrStationName']
            arrTime = item['arrTime']
            arrDate = item['extraBeanMap']['arrDate']

            # 起点信息
            dptStation = item['dptStationName']
            dptTime = item['dptTime']
            dptDate = item['extraBeanMap']['dptDate']

            # 车次信息
            intervalTime = item['extraBeanMap']['interval']
            intervalMiles = item['extraBeanMap']['intervalMiles']
            try:
                trainType = item['trainType']
            except:
                trainType = None
            trainNo = item['trainNo']
            startSaleTime = item['extraBeanMap']['startSaleTime']

            # 座位信息
            saleId = item['saleStatus']['saleId']
            try:
                note = item['saleStatus']['note']
            except:
                note = None
            saleStatus = item['saleStatus']['desc']
            seats = item['seats']
            seats_type = []
            seats_price = []
            seats_remain = []
            seats_status = []
            for type in seats:
                seats_type.append(type)
                seats_price.append(seats[type]['price'])
                seats_remain.append(seats[type]['count']) if seats[type]['count'] != -1 else seats_remain.append('已售空')
                if seats[type]['seatMap']['ticketNumStatus'] == 3 or seats[type]['seatMap']['ticketNumStatus'] == 1:
                    seats_status.append('可抢票')
                elif seats[type]['seatMap']['ticketNumStatus'] == 2:
                    seats_status.append('可购票')
                elif seats[type]['seatMap']['ticketNumStatus'] == 6 and saleId != 30:
                    seats_status.append('可预约抢票')
                    seats_remain.pop(-1)
                    seats_remain.append(100)
                else:
                    seats_status.append('')

            print('========================================================================')
            print('车次：' + trainNo + '\t' + trainType) if trainType else print('车次：' + trainNo + '\t')
            print(
                dptStation + ' ' + dptDate + ' ' + dptTime + '\t>>>>> ' + intervalTime + ' >>>>>>\t' + arrStation + ' ' + arrDate + ' ' + arrTime)
            print('\n*' + saleStatus + '\t' + note + '\t' + startSaleTime + '\n') if note else print(
                '\n*' + saleStatus + '\n')
            for i in range(0, len(seats_type)):
                print(seats_type[i] + '\t' + '￥' + str(seats_price[i]) + '\t' + '余票：' + str(seats_remain[i]) + '\t' +
                      seats_status[i])
            print('\n')

            purchasable_type = []
            for i in range(0, len(seats_type)):
                if seats_status[i] == '可购票' or seats_status[i] == "可预约抢票":
                    purchasable_type.append((seats_type[i], seats_price[i], seats_status[i], seats_remain[i]))
                elif isinstance(seats_remain[i], int) and seats_status[i] == "可抢票":
                    if 0 < seats_remain[i]:
                        purchasable_type.append((seats_type[i], seats_price[i], seats_status[i], seats_remain[i]))
            if purchasable_type:
                data = {
                    'dptHm': dptTime,
                    'starttime': dptDate,
                    'fromstation': dptStation,
                    'tostation': arrStation,
                    'arrHm': arrTime,
                    'endtime': arrDate,

                    'train': trainNo,
                    'seat': purchasable_type,
                    'trainDistance': intervalMiles,
                    'trainDuration': item['lishiValue'],
                    'note': note,
                    'startSaleTime': startSaleTime
                }
                self.DATA.append(data)

    def form_post(self):
        count = 0
        self.Menu = []
        if not self.DATA:
            print("\n* * * 无可购买车次！")
            return
        print('\n========================================可购票车次如下=======================================\n')
        for i in range(0, len(self.DATA)):
            for j in range(0, len(self.DATA[i]['seat'])):
                count += 1
                print('编号：', count, end='')
                print('\t车次：' + self.DATA[i]['train'] + '\t由 ' + self.DATA[i]['fromstation'] + ' 到 ' + self.DATA[i][
                    'tostation'], end='')
                print('   出发时间：' + self.DATA[i]['starttime'] + ' ' + self.DATA[i]['dptHm'] + '   ' +
                      self.DATA[i]['seat'][j][0] + '：￥' + str(self.DATA[i]['seat'][j][1]) + '  ' + '余票：' + str(
                    self.DATA[i]['seat'][j][3]) + '  ' + self.DATA[i]['seat'][j][2], end='')
                if self.DATA[i]['seat'][j][2] == '可预约抢票':
                    print('\t开始售票时间：' + self.DATA[i]['startSaleTime'])
                else:
                    print('\n')
                info = {
                    'train': self.DATA[i]['train'],
                    'note': self.DATA[i]['note'],

                    'dptHm': self.DATA[i]['dptHm'],
                    'starttime': self.DATA[i]['starttime'],
                    'arrHm': self.DATA[i]['arrHm'],
                    'endtime': self.DATA[i]['endtime'],

                    'fromstation': self.DATA[i]['fromstation'],
                    'tostation': self.DATA[i]['tostation'],

                    'seat': self.DATA[i]['seat'][j][0],
                    'price': self.DATA[i]['seat'][j][1],
                    'seatStatus': self.DATA[i]['seat'][j][2],
                    'seatsRemain': str(self.DATA[i]['seat'][j][3]),

                    'trainDistance': self.DATA[i]['trainDistance'],
                    'trainDuration': self.DATA[i]['trainDuration'],
                    'startSaleTime': self.DATA[i]['startSaleTime']
                }
                self.Menu.append(info)
            print('\n')

        while True:
            index = int(input("输入要购买的车次编号：")) - 1
            self.ticket_information = '车次：' + self.Menu[index]['train'] + '\t由 ' + self.Menu[index]['fromstation'] \
                                      + ' 到 ' + self.Menu[index]['tostation'] + '出发时间：' + self.Menu[index]['starttime'] \
                                      + ' ' + self.Menu[index]['dptHm'] + '  ' + self.Menu[index]['seat'] \
                                      + '：￥' + str(self.Menu[index]['price'])
            print(self.ticket_information)
            choice = input('\n确认购买？(y/n)')
            if choice == 'y':
                self.index = index
                break

        self.url = 'http://tieyo.trade.qunar.com/site/booking/purchaseCheck.jsp'
        self.post_data = [
            ('insuranceCorpCode', 'TK'),
            ('trainSeat', self.Menu[index]['seat']),
            ('ticketCount', '1'),
            ('trainFrom', self.Menu[index]['fromstation']),
            ('trainTo', self.Menu[index]['tostation']),
            ('trainStartTime',
             self.Menu[index]['starttime'].replace('-', '') + self.Menu[index]['dptHm'].replace(':', '')),
            ('trainDistance', self.Menu[index]['trainDistance']),
            ('trainDuration', self.Menu[index]['trainDuration']),
            ('trainNo', self.Menu[index]['train']),
            ('ex_track', 'noextrack'),
            # ('pricesInformation', self.Menu[index]['seat']+':'+str(self.Menu[index]['price'])),
            ('isCheckPrice', '0'),
            ('needCheckHistoryOrder', 'false'),
            ('pTicketType_0', '1'),
            ('pName_0', self.pName),
            ('pCertType_0', '0'),
            ('pCertNo_0', self.pIdNo),
            ('pGender_0', self.pGender),
            ('pBirthDate_0', self.pBirthday),
            ('pInsureNo', self.pInsureNo),
            ('contact', 'on'),
            ('contact_name', self.cName),
            ('contact_phone', self.cPhone),
            ('license', 'on'),
            ('paramjson',
             '{"contactusers":[],"consumerusers":[{"usersource":"train","credentialses":[{"credentialstype":1,"credentialsid":115716894,"credentialsno":"511126199908160014"}],"name":"张蔚鹏","id":"119571228","contactid":"119571228","gender":"1","birthday":"1999-08-16"}]}'),
            ('paramjson',
             '{"consumerusers":[],"contactusers":[{"contactid":"119571228","usersource":"train","mobile":"18190687825","name":"张蔚鹏"}]}'),
            ('passenger_member', 'gjn'),
            ('isRecommendPaper', 'false'),
            ('isNeedPaper', 'false'),
            ('expressPrice', '0'),
            ('seatSpecifiedCount', '0'),
            ('acceptOtherSeat', 'false'),
            ('ticketToStationSelected', 'false')
        ]
        self.headers = {
            'Host': 'tieyo.trade.qunar.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'origin': 'https://tieyo.trade.qunar.com',
            'Accept-Encoding': 'gzip, deflate',
            'x-requested-with': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': str(len(urlencode(self.post_data)))
        }

    def update_data(self):
        self.get_info_single_way()
        for item in self.data:
            match_case = item['dptStationName'] == self.Menu[self.index]['fromstation'] and item['arrStationName'] == \
                         self.Menu[self.index]['tostation'] and item['trainNo'] == self.Menu[self.index]['train'] and \
                         item['dptTime'] == self.Menu[self.index]['dptHm']
            if match_case:
                seats = item['seats']
                for type in seats:
                    if type == self.Menu[self.index]['seat']:
                        seats_remain = seats[type]['count'] if seats[type]['count'] != -1 else '已售空'
        return True if seats_remain != '已售空' else False

    def purchase_ticket(self, No):
        self.purchase_status = False
        print("\n进程%s\t正在提交订单信息\t当前时间：%s" % ((No + 1), datetime.datetime.now()))
        error_count = 1
        retry_count = 0

        while True:
            while retry_count < 3:
                response = requests.post(self.url, data=self.post_data, headers=self.headers)
                if "orderDetailUrl" in response.text:
                    print("\n进程%s\t提交订单信息成功，请及时前往去哪儿网支付！" % (No + 1))
                    self.purchase_status = True
                    break
                else:
                    retry_count += 1
            if self.purchase_status == True:
                break
            else:
                print(response.text)
                if error_count == 3:
                    print('抱歉，进程%s抢票失败！' % (No + 1))
                    break
                remain_seat = self.update_data()
                if not remain_seat:
                    break
                error_count += 1
        """
        while retry_count < 3:
            requests.post(self.url, data=self.post_data, headers=self.headers)
            retry_count += 1
        """

    def check(self):
        if self.purchase_status == True:
            self.send_email()
            wait = input("\n输入任意键退出...")
            exit()

    def send_email(self):
        try:
            smtp = smtplib.SMTP('smtp.163.com')
            smtp.starttls()
            smtp.login('jeffzhang0816@163.com', 'Zwp990816')
            sender = 'jeffzhang0816@163.com'
            receiver = '570972004@qq.com'

            msg = email.mime.multipart.MIMEMultipart()

            msg['Subject'] = '抢票'
            msg['From'] = sender
            msg['To'] = receiver
            content = '提交订单信息成功:\t%s\n，请及时前往去哪儿网支付' % self.ticket_information if self.purchase_status else '抱歉，抢票失败！'
            txt = email.mime.text.MIMEText(content)
            msg.attach(txt)

            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()
            print("发送邮件成功！")
        except:
            print('发送邮件失败！')

    def rob_ticket(self):
        schedule = sched.scheduler(time.time, time.sleep)

        startSaleTime = self.Menu[self.index]['startSaleTime']
        startSaleTime = datetime.datetime.strptime(startSaleTime, '%Y-%m-%d %H:%M')
        month = startSaleTime.month
        day = startSaleTime.day

        now = datetime.datetime.now()

        if now.month == month and now.day == day:
            time_before_start = int(round((startSaleTime - now).total_seconds()))
            print("\n开始售票时间为：%s\t还有\t%s秒\t开始抢票..." % (startSaleTime, str(time_before_start)))
            schedule.enter(time_before_start - 0.5, 0, self.multiprocess, ())
            schedule.run()

        else:
            print("\n开始售票时间为\t%s\t请在购票的当日打开此程序！" % startSaleTime)
            return

    def multiprocess(self):
        p = Pool(4)
        for i in range(4):
            p.apply_async(self.purchase_ticket(i))
            # p.apply_async(self.purchase_ticket(i), callback=self.check())
        self.send_email()

    def run(self):
        self.connect_database()
        self.get_info_passenger()
        print("\n正在获取车票信息...")
        self.get_info_single_way()
        self.parse_and_show_data()
        self.form_post()
        if self.Menu[self.index]['seatStatus'] == '可预约抢票':
            self.rob_ticket()
        else:
            self.multiprocess()
        self.check()


if __name__ == '__main__':
    booking = Book_Ticket()
    booking.run()




