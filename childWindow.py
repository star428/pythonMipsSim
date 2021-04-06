from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication, QWidget, QPushButton, QGridLayout, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import sys

from Lexical_analyzer import LexicalAnalyzer

class SummaryWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.TextEdit = QTextEdit()
        self.setCentralWidget(self.TextEdit)

        self.resize(500, 500)
        self.setWindowTitle("data summary")

    def getMessage(self, data):
        self.TextEdit.setText(data)

class CodeWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.TextEdit = QTextEdit()
        self.setCentralWidget(self.TextEdit)

        self.resize(500, 500)
        self.setWindowTitle("code")

    def getMessage(self, data):
        self.analyser = LexicalAnalyzer(data)
        self.TextEdit.setText(self.analyser.returnCodeAnalyseStr())
