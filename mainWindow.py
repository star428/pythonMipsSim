from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QWidget, QPushButton, QGridLayout, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import sys

from childWindow import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.code = 0
        self.initUI()

    def initUI(self):
        # 导入文件的操作
        openFile = QAction(QIcon('open.png'),'open file', self)
        openFile.setStatusTip('open new file')
        openFile.triggered.connect(self.LoadCode)

        # 打开summary窗口的操作
        openSummary = QAction(QIcon('open.png'),'summary', self)
        openSummary.setStatusTip('open summary child window')
        openSummary.triggered.connect(self.openSummaryWindow)

        # 打开code窗口的操作
        openCode = QAction(QIcon('open.png'),'code', self)
        openCode.setStatusTip('open code child window')
        openCode.triggered.connect(self.openCodeWindow)

        # 增加第menu
        menuBar = self.menuBar()

        MenuOne = menuBar.addMenu('&function')
        MenuOne.addAction(openFile)

        MenuTwo = menuBar.addMenu('otherwindow')
        MenuTwo.addAction(openSummary)
        MenuTwo.addAction(openCode)

        # 大小调整
        self.setGeometry(300, 600, 600, 600)
        self.setWindowTitle('MipsSim')

    def LoadCode(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', '.')# 直接打开本文件夹

        if fname[0]:

            with open(fname[0], 'r', encoding='utf-8') as file:
                self.code = file.read()
                self.winCode.getMessage(self.code)

    def openSummaryWindow(self):
        self.winSummary = SummaryWin()
        self.winSummary.show()

    def openCodeWindow(self):
        self.winCode = CodeWin()
        self.winCode.show()
