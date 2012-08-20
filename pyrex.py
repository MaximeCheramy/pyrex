#!/usr/bin/python
# coding=utf-8

from PyQt4.QtGui import QApplication

from gui import MainWindow

if __name__ == '__main__':
    app = QApplication([])
    
    window = MainWindow()
    window.show()
    
    app.exec_()
