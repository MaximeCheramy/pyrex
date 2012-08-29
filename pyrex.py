#!/usr/bin/python
# coding=utf-8

from PyQt4.QtGui import QApplication

from gui import MainWindow
from configuration import Configuration

if __name__ == '__main__':
    app = QApplication([])
    
    print "On loade la config du GUI"
    Configuration.load_config()

    window = MainWindow()
    window.show()
    
    app.exec_()
