#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QTableWidgetItem

from sharedirs import SharedirsGet

class TabShares(QWidget):
    sharedirsReceived = pyqtSignal(list)

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)

        PyQt4.uic.loadUi('ui/shares.ui', self)
        self.table_sharedirs.resizeColumnsToContents()
        
        self.sharedirsReceived.connect(self.set_shares)
        self.sharedirs_get = None

    def update_sharedirs(self):
        if self.sharedirs_get is None:
            self.sharedirs_get = SharedirsGet()
            self.sharedirs_get.do_get(self.sharedirsReceived.emit)

    def add_share(self, sharedir):
        rows = self.table_sharedirs.rowCount()
        self.table_sharedirs.insertRow(rows)
        self.table_sharedirs.setItem(rows, 0, QTableWidgetItem(sharedir.name))
        self.table_sharedirs.setItem(rows, 1, QTableWidgetItem(sharedir.path))


    def set_shares(self, sharedirs):
        while self.table_sharedirs.rowCount():
            self.table_sharedirs.removeRow(0)
        for sharedir in sharedirs:
            self.add_share(sharedir)

        self.sharedirs_get = None
        
    def resizeEvent(self, event):
        maxSize = self.table_sharedirs.size().width()
        # Nom du partage : 35%
        self.table_sharedirs.horizontalHeader().resizeSection(0, maxSize*.35)
        event.accept() 
    
