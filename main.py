# coding=utf-8


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainWidget import *
import threading


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())

