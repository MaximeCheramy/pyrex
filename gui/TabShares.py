#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QTableWidgetItem, QFileDialog

from sharedirs import SharedirsGet, ShareDir, SharedirsSet

class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self, string, sharedir):
        QTableWidgetItem.__init__(self, string)
        self.sharedir = sharedir
        
class TabShares(QWidget):
    sharedirsReceived = pyqtSignal(list)

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)
        # Load de l'UI
        PyQt4.uic.loadUi('ui/shares.ui', self)
        self.table_sharedirs.resizeColumnsToContents()
        # Signaux
        self.sharedirsReceived.connect(self.set_shares)
        self.table_sharedirs.itemChanged.connect(self.get_modif_name)
        self.table_sharedirs.itemActivated.connect(self.get_modif_path)
        # Vars
        self.sharedirs_get = None
        self.sharedirs_set = None
        self.sharedirs = []

    def update_sharedirs(self):
        if self.sharedirs_get is None:
            self.sharedirs_get = SharedirsGet()
            self.sharedirs_get.do_get(self.sharedirsReceived.emit)

    def add_share(self, sharedir):
        rows = self.table_sharedirs.rowCount()
        self.table_sharedirs.insertRow(rows)
        self.table_sharedirs.setItem(rows, 0, MyQTableWidgetItem(sharedir.name, sharedir))
        self.table_sharedirs.setItem(rows, 1, QTableWidgetItem(sharedir.path))
        self.table_sharedirs.item(rows, 1).setFlags(self.table_sharedirs.item(rows, 1).flags() ^ Qt.ItemIsEditable)
        self.sharedirs.append(sharedir)

    def set_shares(self, sharedirs):
        self.sharedirs = []
        while self.table_sharedirs.rowCount():
            self.table_sharedirs.removeRow(0)
        for sharedir in sharedirs:
            self.add_share(sharedir)
        self.sharedirs_get = None
        self.sharedirs_set = None
                  
    def set_sharedirs(self):
        self.sharedirs_set = SharedirsSet()
        self.sharedirs_set.do_set(self.sharedirs, self.sharedirsReceived.emit)
    
    def add_directory(self):
        directory = QFileDialog.getExistingDirectory(self)
        sharedir = ShareDir(unicode(directory.split("/")[-1].toUtf8(), 'utf-8') , unicode(directory.toUtf8(), 'utf-8'))
        self.add_share(sharedir)
        self.set_sharedirs()
                
    def get_sharedir(self):
        row = self.table_sharedirs.currentRow()
        try:
            return self.table_sharedirs.item(row, 0).sharedir   
        except AttributeError:
            return None
         
    def suppr_directory(self):
        sharedir = self.get_sharedir()
        if sharedir:
            self.sharedirs.remove(sharedir)
            self.set_sharedirs()
            
    def get_modif_name(self, item):
        row = item.row()
        sharedir = self.table_sharedirs.item(row, 0).sharedir
        try:
            self.sharedirs.remove(sharedir)
            self.sharedirs.append(ShareDir(unicode(self.table_sharedirs.item(row, 0).text().toUtf8(), 'utf-8'), sharedir.path))
            self.set_sharedirs()
        except ValueError:
            pass
                    
    # TODO : quand on fait "annuler" ce serait pas mal si ça pouvait annuler :)                
    def get_modif_path(self, item):
        row = item.row()
        column = item.column()
        if column == 1:
            sharedir = self.table_sharedirs.item(row, 0).sharedir
            try:
                self.sharedirs.remove(sharedir)
                self.sharedirs.append(ShareDir(sharedir.name, unicode(QFileDialog.getExistingDirectory(self).toUtf8(), 'utf-8')))
                self.set_sharedirs()
            except ValueError:
                pass
    
    def resizeEvent(self, event):
        maxSize = self.table_sharedirs.size().width()
        # Nom du partage : 35%
        self.table_sharedirs.horizontalHeader().resizeSection(0, maxSize*.35)
        event.accept() 
