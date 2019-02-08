# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 353)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.keywordText = QtWidgets.QLineEdit(self.centralwidget)
        self.keywordText.setObjectName("keywordText")
        self.gridLayout.addWidget(self.keywordText, 0, 0, 1, 2)
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setStyleSheet("font: 12pt \"黑体\";")
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 0, 2, 1, 1)
        self.heaven = QtWidgets.QCheckBox(self.centralwidget)
        self.heaven.setObjectName("heaven")
        self.gridLayout.addWidget(self.heaven, 1, 0, 2, 1)
        self.hd_radio = QtWidgets.QCheckBox(self.centralwidget)
        self.hd_radio.setObjectName("hd_radio")
        self.gridLayout.addWidget(self.hd_radio, 2, 1, 1, 2)
        self.btZhijia = QtWidgets.QCheckBox(self.centralwidget)
        self.btZhijia.setObjectName("btZhijia")
        self.gridLayout.addWidget(self.btZhijia, 3, 0, 1, 1)
        self.hd_mp4 = QtWidgets.QCheckBox(self.centralwidget)
        self.hd_mp4.setObjectName("hd_mp4")
        self.gridLayout.addWidget(self.hd_mp4, 3, 1, 1, 1)
        self.chinese_hd = QtWidgets.QCheckBox(self.centralwidget)
        self.chinese_hd.setObjectName("chinese_hd")
        self.gridLayout.addWidget(self.chinese_hd, 4, 0, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 5, 0, 1, 3)
        self.resultTable = QtWidgets.QTableWidget(self.centralwidget)
        self.resultTable.setObjectName("resultTable")
        self.resultTable.setColumnCount(0)
        self.resultTable.setRowCount(0)
        self.gridLayout.addWidget(self.resultTable, 6, 0, 1, 3)
        self.searchResult = QtWidgets.QLabel(self.centralwidget)
        self.searchResult.setText("")
        self.searchResult.setAlignment(QtCore.Qt.AlignCenter)
        self.searchResult.setObjectName("searchResult")
        self.gridLayout.addWidget(self.searchResult, 3, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.searchButton.clicked.connect(MainWindow.searchButton_clicked)
        self.resultTable.cellClicked['int','int'].connect(MainWindow.cell_clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "电影资源搜索器        By Ramond.Z"))
        self.searchButton.setText(_translate("MainWindow", "搜索"))
        self.heaven.setText(_translate("MainWindow", "来源1：电影天堂"))
        self.hd_radio.setText(_translate("MainWindow", "来源2：高清电台(资源贼多，搜索贼慢)"))
        self.btZhijia.setText(_translate("MainWindow", "来源3：BT之家"))
        self.hd_mp4.setText(_translate("MainWindow", "来源4：高清MP4吧"))
        self.chinese_hd.setText(_translate("MainWindow", "来源5：中国高清网"))

import source
