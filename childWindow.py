from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QLineEdit,
    QAction, QFileDialog, QApplication, QWidget, QPushButton, QGridLayout, QLabel)
from PyQt5.QtGui import QIcon, QFont, QPainter, QColor, QBrush
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
import sys

from Lexical_analyzer import LexicalAnalyzer, buildUpInst

class SummaryWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.TextEdit = QTextEdit()
        self.setCentralWidget(self.TextEdit)

        self.setGeometry(900, 300, 600, 600)
        self.setWindowTitle("data summary")

    def getMessage(self, cpu):
        # 开始构建输出文本
        str1 = ""
        str1 = str1 + "周期数：" + str(cpu.clock) + "\n"
        if cpu.isComlete is True:
            str1 = str1 + "是否完成：" + "YES" + "\n"
        else:
            str1 = str1 + "是否完成：" + "NO" + "\n"

        str1 = str1 + "----------(统计能运行到EX段的指令)----------" + "\n"
        str1 = str1 + "lw指令数：" + str(cpu.lw_count) + "\n"
        str1 = str1 + "sw指令数：" + str(cpu.sw_count) + "\n"
        str1 = str1 + "add指令数：" + str(cpu.add_count) + "\n"
        str1 = str1 + "bnez指令数：" + str(cpu.bnez_count) + "\n"

        str1 = str1 + "--------------------" + "\n"
        str1 = str1 + "lw停顿：" + str(cpu.load_stop_count) + "\n"
        str1 = str1 + "add停顿：" + str(cpu.add_stop_count) + "\n"
        str1 = str1 + "bnez停顿：" + str(cpu.bnez_stop_count) + "\n"

        self.TextEdit.setText(str1)

class CodeWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.TextEdit = QTextEdit()
        self.setCentralWidget(self.TextEdit)

        self.setGeometry(1500, 300, 600, 600)
        self.setWindowTitle("code")

    def getMessage(self, data):
        self.analyser = LexicalAnalyzer(data)

        self.TextEdit.setText(self.analyser.returnStrCode())

class PipeLineWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        label_PC_reg = QLabel(self)
        label_PC_reg.setText("PC")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_PC_reg.setStyleSheet("color:black")
        label_PC_reg.move(850, 60)
        label_PC_reg.setFont(QFont("Courier New", 12, QFont.Bold))


        label_IF = QLabel(self)
        label_IF.setText("IF")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_IF.setStyleSheet("color:black")
        label_IF.move(850, 210)
        label_IF.setFont(QFont("Courier New", 12, QFont.Bold))

        label_IF_ID_reg = QLabel(self)
        label_IF_ID_reg.setText("IF/ID")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_IF_ID_reg.setStyleSheet("color:black")
        label_IF_ID_reg.move(850, 360)
        label_IF_ID_reg.setFont(QFont("Courier New", 12, QFont.Bold))

        label_ID = QLabel(self)
        label_ID.setText("ID")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_ID.setStyleSheet("color:black")
        label_ID.move(850, 510)
        label_ID.setFont(QFont("Courier New", 12, QFont.Bold))

        label_ID_EX_reg = QLabel(self)
        label_ID_EX_reg.setText("ID/EX")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_ID_EX_reg.setStyleSheet("color:black")
        label_ID_EX_reg.move(850, 660)
        label_ID_EX_reg.setFont(QFont("Courier New", 12, QFont.Bold))

        label_EX = QLabel(self)
        label_EX.setText("EX")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_EX.setStyleSheet("color:black")
        label_EX.move(850, 810)
        label_EX.setFont(QFont("Courier New", 12, QFont.Bold))

        label_EX_MEM_reg = QLabel(self)
        label_EX_MEM_reg.setText("EX/MEM")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_EX_MEM_reg.setStyleSheet("color:black")
        label_EX_MEM_reg.move(850, 960)
        label_EX_MEM_reg.setFont(QFont("Courier New", 12, QFont.Bold))

        label_MEM = QLabel(self)
        label_MEM.setText("MEM")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_MEM.setStyleSheet("color:black")
        label_MEM.move(850, 1110)
        label_MEM.setFont(QFont("Courier New", 12, QFont.Bold))

        label_MEM_WB_reg = QLabel(self)
        label_MEM_WB_reg.setText("MEM/WB")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_MEM_WB_reg.setStyleSheet("color:black")
        label_MEM_WB_reg.move(850, 1260)
        label_MEM_WB_reg.setFont(QFont("Courier New", 12, QFont.Bold))

        label_WB = QLabel(self)
        label_WB.setText("WB")
        # label.adjustSize() # 调整label大小以显示字体全部
        label_WB.setStyleSheet("color:black")
        label_WB.move(850, 1410)
        label_WB.setFont(QFont("Courier New", 12, QFont.Bold))
        # 上面是要直接显示的

        # 要填入的,reg_write都是中间寄存器写，其他就是5个段

        self.label_PC_reg_write = QLabel(self)
        # self.label_PC_IF.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_PC_reg_write.setStyleSheet("color:black")
        self.label_PC_reg_write.move(300, 70)
        self.label_PC_reg_write.resize(300,20)
        self.label_PC_reg_write.setFont(QFont("Courier New", 12, QFont.Bold))


        self.label_PC_IF = QLabel(self)
        # self.label_PC_IF.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_PC_IF.setStyleSheet("color:black")
        self.label_PC_IF.move(300, 220)
        self.label_PC_IF.resize(300,20)
        self.label_PC_IF.setFont(QFont("Courier New", 12, QFont.Bold))


        self.label_IF_ID_reg_write = QLabel(self)
        # self.label_IF_ID.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_IF_ID_reg_write.setStyleSheet("color:black")
        self.label_IF_ID_reg_write.move(200, 370)
        self.label_IF_ID_reg_write.resize(500,20)
        self.label_IF_ID_reg_write.setFont(QFont("Courier New", 12, QFont.Bold))


        self.label_IF_ID = QLabel(self)
        # self.label_IF_ID.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_IF_ID.setStyleSheet("color:black")
        self.label_IF_ID.move(300, 520)
        self.label_IF_ID.resize(300,20)
        self.label_IF_ID.setFont(QFont("Courier New", 12, QFont.Bold))

        self.label_ID_EX_reg_write = QLabel(self)
        # self.label_IF_ID.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_ID_EX_reg_write.setStyleSheet("color:black")
        self.label_ID_EX_reg_write.move(200, 670)
        self.label_ID_EX_reg_write.resize(500,20)
        self.label_ID_EX_reg_write.setFont(QFont("Courier New", 12, QFont.Bold))

        self.label_ID_EX = QLabel(self)
        # self.label_IF_ID.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_ID_EX.setStyleSheet("color:black")
        self.label_ID_EX.move(300, 820)
        self.label_ID_EX.resize(300,20)
        self.label_ID_EX.setFont(QFont("Courier New", 12, QFont.Bold))

        self.label_EX_MEM_reg_write = QLabel(self)
        # self.label_IF_ID.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_EX_MEM_reg_write.setStyleSheet("color:black")
        self.label_EX_MEM_reg_write.move(200, 970)
        self.label_EX_MEM_reg_write.resize(500,20)
        self.label_EX_MEM_reg_write.setFont(QFont("Courier New", 12, QFont.Bold))

        self.label_EX_MEM = QLabel(self)
        # self.label_IF_ID.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_EX_MEM.setStyleSheet("color:black")
        self.label_EX_MEM.move(300, 1120)
        self.label_EX_MEM.resize(300,20)
        self.label_EX_MEM.setFont(QFont("Courier New", 12, QFont.Bold))

        self.label_MEM_WB_reg_write = QLabel(self)
        # self.label_IF_ID.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_MEM_WB_reg_write.setStyleSheet("color:black")
        self.label_MEM_WB_reg_write.move(200, 1270)
        self.label_MEM_WB_reg_write.resize(500,20)
        self.label_MEM_WB_reg_write.setFont(QFont("Courier New", 12, QFont.Bold))

        self.label_MEM_WB = QLabel(self)
        # self.label_IF_ID.setText("hello")
        # self.label_IF_ID.adjustSize() # 调整label大小以显示字体全部
        self.label_MEM_WB.setStyleSheet("color:black")
        self.label_MEM_WB.move(300, 1420)
        self.label_MEM_WB.resize(300,20)
        self.label_MEM_WB.setFont(QFont("Courier New", 12, QFont.Bold))


        self.setGeometry(2100, 300, 1000, 1500)
        self.setWindowTitle("PipeLine")

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()


    def drawRectangles(self, qp):

        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

        qp.setBrush(QColor('#ffe4bad4'))# 前两位表示透明度，后两位就是正常6位16进制数
        qp.drawRect(50, 25, 700, 100)

        qp.setBrush(QColor('#fff0e4d7'))# 前两位表示透明度，后两位就是正常6位16进制数
        qp.drawRect(200, 175, 400, 100)

        qp.setBrush(QColor("#ffedffec"))
        qp.drawRect(50, 325, 700, 100)

        qp.setBrush(QColor("#ffff7171"))
        qp.drawRect(200, 475, 400, 100)

        qp.setBrush(QColor("#fff6dfeb"))
        qp.drawRect(50, 625, 700, 100)

        qp.setBrush(QColor("#ff98ddca"))
        qp.drawRect(200, 775, 400, 100)

        qp.setBrush(QColor("#ffe4bad4"))
        qp.drawRect(50, 925, 700, 100)

        qp.setBrush(QColor("#ffffd3b4"))
        qp.drawRect(200, 1075, 400, 100)

        qp.setBrush(QColor("#ffff8882"))
        qp.drawRect(50, 1225, 700, 100)

        qp.setBrush(QColor("#ffffaaa7"))
        qp.drawRect(200, 1375, 400, 100)


    def getMessage(self, cpu):

        if cpu is None: # 清空操作
            self.label_PC_IF.setText("")
            self.label_IF_ID.setText("")
            self.label_ID_EX.setText("")
            self.label_EX_MEM.setText("")
            self.label_MEM_WB.setText("")

            self.label_PC_reg_write.setText("")
            self.label_IF_ID_reg_write.setText("")
            self.label_ID_EX_reg_write.setText("")
            self.label_EX_MEM_reg_write.setText("")
            self.label_MEM_WB_reg_write.setText("")

            return 0

        if cpu.PC.out_PC() < len(cpu.IM.mem):
            self.label_PC_IF.setText(buildUpInst(cpu.IM.getInst(cpu.PC.out_PC())))
        else:
            self.label_PC_IF.setText("")


        if cpu.IF_ID_reg.IR is None:
            self.label_IF_ID.setText("")
        else:
            self.label_IF_ID.setText(buildUpInst(cpu.IF_ID_reg.IR))


        if cpu.ID_EX_reg.IR is None:
                self.label_ID_EX.setText("")
        else:
            self.label_ID_EX.setText(buildUpInst(cpu.ID_EX_reg.IR))


        if cpu.EX_MEM_reg.IR is None:
            self.label_EX_MEM.setText("")
        else:
            self.label_EX_MEM.setText(buildUpInst(cpu.EX_MEM_reg.IR))


        if cpu.MEM_WB_reg.IR is None:
            self.label_MEM_WB.setText("")
        else:
            self.label_MEM_WB.setText(buildUpInst(cpu.MEM_WB_reg.IR))

    def getMessageAfter(self, cpu):
        if cpu.PC.out_PC() >= len(cpu.IM.mem):
            self.label_PC_reg_write.setText("")
        else:
            self.label_PC_reg_write.setText(str(cpu.PC.out_PC()))

        if cpu.IF_ID_reg.IR is None:
            self.label_IF_ID_reg_write.setText("")
        else:
            NPC = ""
            if cpu.IF_ID_reg.NPC is not None:
                NPC = str(cpu.IF_ID_reg.NPC)

            self.label_IF_ID_reg_write.setText("NPC: " + NPC + "  " + \
                buildUpInst(cpu.IF_ID_reg.IR))

        if cpu.ID_EX_reg.IR is None:
            self.label_ID_EX_reg_write.setText("")
        else:
            A = ""
            B = ""
            imm = ""

            if cpu.ID_EX_reg.A is not None:
                A = str(cpu.ID_EX_reg.A)

            if cpu.ID_EX_reg.B is not None:
                B = str(cpu.ID_EX_reg.B)

            if cpu.ID_EX_reg.imm is not None:
                imm = str(cpu.ID_EX_reg.imm)

            self.label_ID_EX_reg_write.setText("A:" + A + ", " + "B:" + B + \
                ", " + "imm:" + imm + ", " + "IR:" + buildUpInst(cpu.ID_EX_reg.IR))

        if cpu.EX_MEM_reg.IR is None:
            self.label_EX_MEM_reg_write.setText("")
        else:
            ALUo = ""
            B = ""
            if cpu.EX_MEM_reg.ALUo is not None:
                ALUo = str(cpu.EX_MEM_reg.ALUo)
            if cpu.EX_MEM_reg.B is not None:
                B = str(cpu.EX_MEM_reg.B)

            self.label_EX_MEM_reg_write.setText("ALUo:" + ALUo + ", " + \
                "B:" + B + ", " + "IR:" + buildUpInst(cpu.EX_MEM_reg.IR))

        if cpu.MEM_WB_reg.IR is None:
            self.label_MEM_WB_reg_write.setText("")
        else:
            LMD = ""
            ALUo = ""

            if cpu.MEM_WB_reg.LMD is not None:
                LMD = str(cpu.MEM_WB_reg.LMD)

            if cpu.MEM_WB_reg.ALUo is not None:
                ALUo = str(cpu.MEM_WB_reg.ALUo)

            self.label_MEM_WB_reg_write.setText("LMD:" + LMD + ", " + \
                "ALUo:" + ALUo + ", " + "IR:" + buildUpInst(cpu.MEM_WB_reg.IR))








class RegFileWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 同样直接由纯文本显示
        self.TextEdit = QTextEdit()
        self.setCentralWidget(self.TextEdit)


        self.setGeometry(900, 900, 600, 600)
        self.setWindowTitle("RegFile")

    def getMessage(self, data):
        # data为regfile中的rf（是dict）
        strOne = ""
        for key in data.keys():
            strOne = strOne + key + ":" + str(data[key])
            if key[1] == 'R':
                strOne = strOne + "    "
            else:
                strOne = strOne + "\n"

        self.TextEdit.setText(strOne)

class DataMemWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 直接由文本展示
        self.TextEdit = QTextEdit()
        self.setCentralWidget(self.TextEdit)


        self.setGeometry(1500, 900, 600, 600)
        self.setWindowTitle("DataMem")

    def getMessage(self, data):
        # get的是DM的mem值（dict）
        strOne = "addr--------data\n"
        for key in data.keys():
            strOne = strOne + str(key) + "--------" + str(data[key]) + "\n"

        self.TextEdit.setText(strOne)


class ErrorMessageWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        label = QLabel(self)
        label.setText("you don't put your code in IM(please quit to load inst)")
        label.adjustSize() # 调整label大小以显示字体全部
        label.setStyleSheet("color:black")
        label.move(0, 10)
        label.setFont(QFont("微软雅黑", 8, QFont.Bold))

        self.setGeometry(300, 300, 500, 100)
        self.setWindowTitle('Error Message')

class ErrorMessageWinTwo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        label = QLabel(self)
        label.setText("not have that address")
        label.adjustSize() # 调整label大小以显示字体全部
        label.setStyleSheet("color:black")
        label.move(0, 10)
        label.setFont(QFont("微软雅黑", 8, QFont.Bold))

        self.setGeometry(300, 300, 500, 100)
        self.setWindowTitle('Error Message')


class PointMessageGet(QWidget):# 获取断点所需的地址和相应的段名
    _signal = QtCore.pyqtSignal(int, str)
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        label_one = QLabel("address")
        label_two = QLabel("frame")

        # 创建两个按钮
        btnYes = QPushButton("yes", self)
        btnYes.resize(btnYes.sizeHint())
        btnYes.clicked.connect(self.setMessage)

        btnNo = QPushButton("no", self)
        btnNo.resize(btnNo.sizeHint())
        btnNo.clicked.connect(self.close)

        # 创建两个文本框
        self.editAddr = QLineEdit()
        self.editFrame = QLineEdit()

        # 开始排版
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(label_one, 0, 0)
        grid.addWidget(self.editAddr, 1, 0)
        grid.addWidget(label_two, 0, 1)
        grid.addWidget(self.editFrame, 1, 1)
        grid.addWidget(btnYes, 2, 0)
        grid.addWidget(btnNo, 2, 1)

        self.setLayout(grid)

        self.resize(600, 100)
        self.setWindowTitle('go to point')

    def setMessage(self):
        addr = int(self.editAddr.text())
        frame = self.editFrame.text()
        self._signal.emit(addr, frame.lower())
        self.close()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = PipeLineWin()
        win.show()
        sys.exit(app.exec_())
