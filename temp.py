# lw $t0,10($t1) sw $t0,10($t1)
# add $t0,$t1,$t2
# BENZ R1,NAME

# 形式诸如string，以行为分界开始词法分析
# cation!!!!!!!!
# 这里的代码知识测试用，最后会全部删除不会备档
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QWidget, QPushButton, QGridLayout, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import sys

class childWindow(QMainWindow):

    def __init__(self):
        super(childWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.TextEdit = QTextEdit()
        self.setCentralWidget(self.TextEdit)

        self.resize(500, 200)
        self.setWindowTitle("DDA Line Setting")

    def getMessage(self, data):
        self.TextEdit.setText(data)


class textInput(QMainWindow):
    def __init__(self):

        super().__init__()

        self.data = False
        self.initUI()

    def initUI(self):

        self.TextEdit = QTextEdit()
        self.setCentralWidget(self.TextEdit)
        self.statusBar()# 底部状态栏

        openFile = QAction(QIcon('open.png'),'open', self)
        openFile.setStatusTip('open new file')
        openFile.triggered.connect(self.showDialog) # 点击的链接函数

        getData = QAction(QIcon('open.png'),'get data', self)
        getData.setStatusTip('return the text data to run')
        getData.triggered.connect(self.getData)

        otherWindow = QAction(QIcon('open.png'),'openNewWindow', self)
        otherWindow.triggered.connect(self.openNewWindow)


        menuBar = self.menuBar()
        fileMenuOne = menuBar.addMenu('&function')
        fileMenuOne.addAction(openFile)
        fileMenuOne.addAction(getData)

        fileMenuTwo = menuBar.addMenu('otherwindow')
        fileMenuTwo.addAction(otherWindow)

        self.setGeometry(300, 600, 600, 1200)
        self.setWindowTitle('text input')

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', '/home')

        if fname[0]:

            with open(fname[0], 'r', encoding='utf-8') as file:
                self.data = file.read()
                self.TextEdit.setText(self.data)
                print(self.data)

    def getData(self):
        self.data = self.TextEdit.toPlainText()
        print(self.data)
        self.w1.getMessage(self.data)

    def openNewWindow(self):
        self.w1 = childWindow()
        self.w1.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = textInput()
    ex.show()
    sys.exit(app.exec_())
