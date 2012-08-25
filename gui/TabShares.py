#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget

class TabShares(QWidget):
    sharesReceived = pyqtSignal(list)

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)

        PyQt4.uic.loadUi('ui/shares.ui', self)
        
        self.sharesReceived.connect(self.set_shares)

    def set_shares(self, shares):
        pass

    
