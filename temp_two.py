import sys
import math
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import (QPixmap, QMovie)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel)

class DemoLabel(QMainWindow):
    def __init__(self, parent=None):
        super(DemoLabel, self).__init__(parent)

        # 设置窗口标题
        self.setWindowTitle("实战PyQt5: QLabel Demo!")
        # 设置窗口大小
        self.resize(400, 240)

        #label1 显示一段文字
        label1 = QLabel(self)
        label1.move(10, 10)
        label1.setText("This is a PyQt5 label widget!")
        label1.adjustSize() #调整尺寸，以完全显示字符串

        #label2 显示一个整数
        label2 = QLabel(self)
        label2.move(10, 30)
        label2.setNum(10000)

        #label3 显示一个小数
        label3 = QLabel(self)
        label3.move(10, 50)
        label3.setNum(math.pi)

        # label4 显示一个图片
        pix = QPixmap(os.path.dirname(__file__) + "/python-logo.png")
        label4 = QLabel(self)
        label4.move(10, 80)
        label4.setFixedSize(pix.width(), pix.height())
        label4.setPixmap(pix)

        # label5 显示一个动画
        movie = QMovie(os.path.dirname(__file__) + "/use-python.gif")
        label5 = QLabel(self)
        label5.move(200, 10)
        label5.setFixedSize(176, 180)
        label5.setMovie(movie)
        movie.start()

        # label6 显示一个超链接
        label6 = QLabel(self)
        label6.move(10, 160)
        label6.setText("<A href='http://www.10qianwan.com/articledetail/www.baidu.com'>欢迎使用百度</a>")
        label6.setToolTip("这是一个超链接标签")
        label6.setOpenExternalLinks(True) # 允许访问超链接

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoLabel()
    window.show()
    sys.exit(app.exec())
