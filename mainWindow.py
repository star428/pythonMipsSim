from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QWidget, QPushButton, QGridLayout, QLabel)
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from  CPU import CPU

from childWindow import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.code = 0

        self.cpu = CPU(None) # 初始IM中的元素是none，到时候判断是否为none即可

        self.initUI()

    def initUI(self):
        # 导入文件的操作
        openFile = QAction(QIcon('open.png'),'open file', self)
        openFile.setStatusTip('open new file')
        openFile.triggered.connect(self.LoadCode)

        # 单步执行操作
        runOneCycle = QAction(QIcon('open.png'),'run one cycle', self)
        runOneCycle.setStatusTip('will run one cycle')
        runOneCycle.triggered.connect(self.runOneCycleFunc)
        # 执行到程序结束
        runToEnd = QAction(QIcon('open.png'),'run to end', self)
        runToEnd.setStatusTip('will run to end')
        runToEnd.triggered.connect(self.runToEndFunc)

        # 执行到断点
        runToPoint = QAction(QIcon('open.png'),'run to point', self)
        runToPoint.setStatusTip('will run to point')
        runToPoint.triggered.connect(self.runToPointFunc)

        # 打开summary窗口的操作
        openSummary = QAction(QIcon('open.png'),'summary', self)
        openSummary.setStatusTip('open summary child window')
        openSummary.triggered.connect(self.openSummaryWindow)

        # 打开code窗口的操作
        openCode = QAction(QIcon('open.png'),'code', self)
        openCode.setStatusTip('open code child window')
        openCode.triggered.connect(self.openCodeWindow)

        # 打开中间寄存if，id等的寄存器
        openPipeLine = QAction(QIcon('open.png'),'pipeline', self)
        openPipeLine.setStatusTip('open PipeLine child window')
        openPipeLine.triggered.connect(self.openPipeLineWindow)

        # 打开regfile
        openRegFile = QAction(QIcon('open.png'),'RegFile', self)
        openRegFile.setStatusTip('open regfile child window')
        openRegFile.triggered.connect(self.openRegFileWindow)

        # 打开DataMem
        openDataMem = QAction(QIcon('open.png'),'DataMem', self)
        openDataMem.setStatusTip('open DataMem child window')
        openDataMem.triggered.connect(self.openDataMemWindow)

        # 设置是否使用forwarding
        useForwarding = QAction(QIcon('open.png'),'forwarding', self, checkable=True)
        useForwarding.setStatusTip('use forwarding')
        useForwarding.setChecked(False)
        useForwarding.triggered.connect(self.setForwarding)
        # 增加第menu
        menuBar = self.menuBar()

        MenuOne = menuBar.addMenu('&function')
        MenuOne.addAction(openFile)
        MenuOne.addAction(runOneCycle)
        MenuOne.addAction(runToEnd)
        MenuOne.addAction(runToPoint)

        MenuTwo = menuBar.addMenu('otherwindow')
        MenuTwo.addAction(openSummary)
        MenuTwo.addAction(openCode)
        MenuTwo.addAction(openPipeLine)
        MenuTwo.addAction(openRegFile)
        MenuTwo.addAction(openDataMem)

        MenuThree = menuBar.addMenu('Tools')
        MenuThree.addAction(useForwarding)

        self.statusBar()
        # 大小调整
        self.setGeometry(300, 300, 863, 842)

        # 展示图片

        self.label = QLabel(self)
        self.label.setFixedSize(863, 812)
        self.label.move(0, 30)

        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )
        jpg = QtGui.QPixmap('image\\bg.jpg').scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        # 展示图片结束

        self.setWindowTitle('MipsSim')

        # 其他窗口展示
        self.winSummary = SummaryWin()

        self.winCode = CodeWin()

        self.winPipeLine = PipeLineWin()

        self.winRegFile = RegFileWin()

        self.winDataMem = DataMemWin()

        self.winSummary.show()
        self.winCode.show()
        self.winPipeLine.show()
        self.winRegFile.show()
        self.winDataMem.show()


    def LoadCode(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', '.')# 直接打开本文件夹

        if fname[0]:

            with open(fname[0], 'r', encoding='utf-8') as file:
                if self.cpu.isForwarding is False:
                    self.cpu = CPU(None)
                else:
                    self.cpu = CPU(None)
                    self.cpu.isForwarding = True
                self.code = file.read()

                # 解析代码同时把解析后的代码放入cpu的IM中
                anaylser = LexicalAnalyzer(self.code)
                self.cpu.IM.initIM(anaylser.returnCodeAnalyse())


                self.winSummary.getMessage(self.cpu)
                self.winCode.getMessage(self.code)
                self.winPipeLine.getMessage(None)
                self.winRegFile.getMessage(self.cpu.RegFile.rf)
                self.winDataMem.getMessage(self.cpu.DM.mem)


    def runOneCycleFunc(self):


        if self.cpu.IM.mem == None:
            self.errorWin = ErrorMessageWin()
            self.errorWin.show()
        else:
            self.winPipeLine.getMessage(self.cpu) # 显示各个流水段当前周期在执行什么指令

            self.cpu.runOneCycle()
            self.cpu.showStation()

            self.winSummary.getMessage(self.cpu)
            self.winPipeLine.getMessageAfter(self.cpu)
            self.winRegFile.getMessage(self.cpu.RegFile.rf)
            self.winDataMem.getMessage(self.cpu.DM.mem)

    def runToEndFunc(self):

        if self.cpu.IM.mem == None:
            self.errorWin = ErrorMessageWin()
            self.errorWin.show()
        else:
            self.cpu.runToEnd()

            self.winSummary.getMessage(self.cpu)
            self.winPipeLine.getMessage(self.cpu)
            self.winPipeLine.getMessageAfter(self.cpu)
            self.winRegFile.getMessage(self.cpu.RegFile.rf)
            self.winDataMem.getMessage(self.cpu.DM.mem)

    def runToPointFunc(self):
        if self.cpu.IM.mem == None:
            self.errorWin = ErrorMessageWin()
            self.errorWin.show()
        else:
            self.pointWin = PointMessageGet()
            self.pointWin.show()

            self.pointWin._signal.connect(self.getPointMessage)


    def getPointMessage(self, addr, frame): # 槽函数，与上个槽信号connect
        cpu = self.cpu.runToPoint(addr, frame)
        # cpu.showStation()
        if cpu is None:
            # print("error")
            self.errorWinTwo = ErrorMessageWinTwo()
            self.errorWinTwo.show()
        else:

            self.winSummary.getMessage(self.cpu)
            self.winPipeLine.getMessage(cpu)
            self.winPipeLine.getMessageAfter(self.cpu)
            self.winRegFile.getMessage(self.cpu.RegFile.rf)
            self.winDataMem.getMessage(self.cpu.DM.mem)

    def openSummaryWindow(self):
        self.winSummary = SummaryWin()
        self.winSummary.show()

    def openCodeWindow(self):
        self.winCode = CodeWin()
        self.winCode.show()

    def openPipeLineWindow(self):
        self.winPipeLine = PipeLineWin()
        self.winPipeLine.show()

    def openRegFileWindow(self):
        self.winRegFile = RegFileWin()
        self.winRegFile.show()

    def openDataMemWindow(self):
        self.winDataMem = DataMemWin()
        self.winDataMem.show()

    def setForwarding(self, state):

        if state:
            self.cpu.isForwarding = True
        else:
            self.cpu.isForwarding = False
