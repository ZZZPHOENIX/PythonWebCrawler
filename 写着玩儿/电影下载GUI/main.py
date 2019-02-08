import sys
import MainWindow
import linkTable
import core
import threading
import source
import titleBar
from queue import Queue
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

threadLock = threading.Lock()

class LinkList(QDialog, linkTable.Ui_Dialog):
    def __init__(self, parent=None):
        super(LinkList, self).__init__(parent)
        self.setupUi(self)

    def listItem_clicked(self, listItem):
        clipboard = QApplication.clipboard()
        clipboard.setText(listItem.text())
        QMessageBox.information(self, "", "已复制下载链接到剪贴板！", QMessageBox.Yes)

    def showList(self, links):
        for i in range(len(links)):
            self.linkList.addItem(QListWidgetItem(links[i]))

    def clear(self):
        self.linkList.clear()

class MainWindow(QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏主窗口边界

        self.setWindowIcon(QIcon(':images/images/icon.png'))

        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)

        self.setupUi(self)

        '爬取“电影天堂”的爬虫'
        self.engine1 = core.MovieHeaven()
        '爬取“高清电台”的爬虫'
        self.engine2 = core.HD_Radio()
        '爬取“BT之家”的爬虫'
        self.engine3 = core.BTzhijia()
        '爬取“高清MP4吧”的爬虫'
        self.engine4 = core.HD_MP4()
        '爬取“中国高清网”的爬虫'
        self.engine5 = core.Chinese_HD()

        self.engineList = [self.engine1,
                           self.engine2,
                           self.engine3,
                           self.engine4,
                           self.engine5]

        '存储所有爬取到的电影信息'
        self.allInfo = list()

        '设置样式'
        self.setStyles()


    def setStyles(self):
        """
        设置窗口样式
        :return:
        """

        '设置电影信息表格格式'
        self.setTable()
        '显示电影下载链接的窗口'
        self.linkList = LinkList()
        self.linkList.setWindowIcon(QIcon(':images/images/icon.png'))
        '初始化搜索进度条'
        self.progressBar.setValue(0)

        '设置按钮样式'
        qss = "QPushButton{border: 2px solid #336699;padding:7px;border-radius:2px;color:#FFFFFF;background:#6699CC}"
        qss += "QPushButton:hover{color:#FFFFFF;background:#99CCFF;}"
        qss += "QPushButton:pressed{color:#FFFFFF;background:#6699CC;}"
        self.searchButton.setStyleSheet(qss)

        '设置输入框样式'
        qss = "QLineEdit{border-style:none;padding:4px;border-radius:2px;border:2px solid #6699CC;}"
        qss += "QLineEdit:focus{border:2px solid #336699;}"
        self.keywordText.setStyleSheet(qss)

        '设置进度条样式'
        qss = "QProgressBar {border: 1px solid #336699; border-radius: 3px; background-color: #FFFFFF; text-align: center;}"
        qss += "QProgressBar::chunk {background-color:#6699CC; width: 20px;}"
        self.progressBar.setStyleSheet(qss)

    def setTable(self):
        """
        设置电影信息表格格式
        :return:
        """
        self.resultTable.setRowCount(len(self.allInfo))
        self.resultTable.setColumnCount(11)
        self.resultTable.setRowCount(0)
        self.resultTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.resultTable.resizeColumnsToContents()
        self.resultTable.horizontalHeader().close()

        '设置滚动条样式'
        file = open('ScrollBarStyle.qss', 'r')
        self.resultTable.verticalScrollBar().setStyleSheet(file.read())
        self.resultTable.horizontalScrollBar().setStyleSheet(file.read())

    def refreshTable(self):
        """
        刷新电影信息表格
        :return:
        """
        self.resultTable.horizontalHeader().show()
        headers = ["来源", "下载链接", "译名", "片名", "年代", "产地", "类别", "语言", "上映日期", "IMDb评分", "豆瓣评分"]
        self.resultTable.setHorizontalHeaderLabels(headers)
        self.resultTable.setRowCount(len(self.allInfo))

        for i in range(len(self.allInfo)):
            source = QTableWidgetItem(self.allInfo[i][10])
            translateName = QTableWidgetItem(self.allInfo[i][0])
            name = QTableWidgetItem(self.allInfo[i][1])
            year = QTableWidgetItem(self.allInfo[i][2])
            location = QTableWidgetItem(self.allInfo[i][3])
            type = QTableWidgetItem(self.allInfo[i][4])
            language = QTableWidgetItem(self.allInfo[i][5])
            releaseDate = QTableWidgetItem(self.allInfo[i][6])
            IMDbScore = QTableWidgetItem(self.allInfo[i][7])
            DoubanScore = QTableWidgetItem(self.allInfo[i][8])
            downloadUrl = QTableWidgetItem("下载链接")

            self.resultTable.setItem(i, 0, source)
            self.resultTable.setItem(i, 1, downloadUrl)
            self.resultTable.setItem(i, 2, translateName)
            self.resultTable.setItem(i, 3, name)
            self.resultTable.setItem(i, 4, year)
            self.resultTable.setItem(i, 5, location)
            self.resultTable.setItem(i, 6, type)
            self.resultTable.setItem(i, 7, language)
            self.resultTable.setItem(i, 8, releaseDate)
            self.resultTable.setItem(i, 9, IMDbScore)
            self.resultTable.setItem(i, 10, DoubanScore)
            self.resultTable.resizeColumnsToContents()

            if self.allInfo[i][10] == "电影天堂":
                color = QColor(178, 220, 245)
            elif self.allInfo[i][10] == "高清电台":
                color = QColor(253, 245, 161)
            elif self.allInfo[i][10] == "BT之家":
                color = QColor(255, 185, 173)
            elif self.allInfo[i][10] == "高清MP4吧":
                color = QColor(226, 242, 213)
            elif self.allInfo[i][10] == "中国高清网":
                color = QColor(249, 238, 211)
            else:
                color = QColor(255, 255, 255)
            for j in range(11):
                self.resultTable.item(i, j).setBackground(QBrush(color))

    def searchButton_clicked(self):
        """
        单击“搜索”按钮爬取电影信息
        :return:
        """
        self.searchResult.setText("正在搜索...")

        for i in range(len(self.engineList)):
            self.engineList[i].refresh()

        self.allInfo = list()
        self.progressBar.setValue(0)

        self.num = 0
        text = self.keywordText.text()
        queue = Queue(0)

        engineStatus = [self.heaven.isChecked(),
                        self.hd_radio.isChecked(),
                        self.btZhijia.isChecked(),
                        self.hd_mp4.isChecked(),
                        self.chinese_hd.isChecked(),]

        self.thread1 = SearchMovies(text, self.engineList, engineStatus, queue)
        self.thread1.signalOut.connect(self.closeLoading)
        self.thread1.start()

        self.thread2 = ParseUrls(self.engineList, engineStatus, queue)
        self.thread2.signalOut.connect(self.setProgress)
        self.thread2.start()

        self.progressBar.setMaximum(self.num)

    def cell_clicked(self, row, column):
        """
        监视单击表格中的“下载链接”栏
        :param row: 行
        :param column: 列
        :return:
        """
        if column == 1:
            self.linkList.show()

            links = self.allInfo[row][9]
            self.linkList.clear()
            self.linkList.showList(links)

    def setProgress(self, status, info, total):
        self.progressBar.setMaximum(total)
        self.progressBar.setValue(status)
        self.allInfo.append(info)
        self.refreshTable()

    def closeLoading(self, num):
        self.num = num
        if self.num == 0:
            self.progressBar.setMaximum(1)
            self.progressBar.setValue(1)
        self.searchResult.setText("共 %s 条搜索结果" % self.num)

class SearchMovies(QThread):
    signalOut = pyqtSignal(int)

    def __init__(self, keyword, engineList, engineStatus, queue):
        super().__init__()
        self.keyword = keyword
        self.num = 0
        self.engineList = engineList
        self.engineStatus = engineStatus
        self.queue = queue

    def run(self):
        if threadLock.acquire():
            for i in range(len(self.engineList)):
                if self.engineStatus[i]:
                    self.engineList[i].keyword = self.keyword
                    if self.engineList[i].searchMovie():
                        self.num += len(self.engineList[i].movieUrlList)
            self.queue.put(self.num)
            self.signalOut.emit(self.num)
        threadLock.release()

class ParseUrls(QThread):
    signalOut = pyqtSignal(int, list, int)

    def __init__(self, engineList, engineStatus, queue):
        super().__init__()
        self.num = 0
        self.engineList = engineList
        self.engineStatus = engineStatus
        self.movieInfo = list()
        self.queue = queue

    def run(self):
        while True:
            if not self.queue.empty():
                if threadLock.acquire():
                    self.num = self.queue.get()
                    threads = []
                    stack = []
                    self.status = 0
                    def count():
                        while self.status != self.num:
                            if len(stack) != 0:
                                self.status += stack.pop(-1)
                                for i in range(len(self.engineList)):
                                    if len(self.engineList[i].movieInfo) != 0:
                                        self.movieInfo = self.engineList[i].movieInfo.pop(0)
                                        self.signalOut.emit(self.status, self.movieInfo, self.num)
                                        break

                    threads.append(threading.Thread(target=count))

                    for i in range(len(self.engineStatus)):
                        if self.engineStatus[i]:
                            t = threading.Thread(target=self.engineList[i].getInfo, args=(stack,))
                            threads.append(t)

                    for t in threads:
                        t.setDaemon(True)
                        t.start()
                    threadLock.release()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = titleBar.FramelessWindow()
    w.setWindowTitle('电影资源搜索器')
    w.setWindowIcon(QIcon(':images/images/icon.png'))
    #w.setFixedSize(QSize(655, 368))
    w.setWidget(MainWindow(w))  # 把自己的窗口添加进来

    #w.setStyleSheet("#MainWindow{border-image:url(./images/background.png);}")

    w.show()

    sys.exit(app.exec_())