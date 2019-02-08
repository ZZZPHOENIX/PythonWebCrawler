# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'linkTable.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.linkList = QtWidgets.QListWidget(Dialog)
        self.linkList.setObjectName("linkList")
        self.gridLayout.addWidget(self.linkList, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.linkList.itemClicked['QListWidgetItem*'].connect(Dialog.listItem_clicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "下载链接"))

