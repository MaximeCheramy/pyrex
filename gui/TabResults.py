# coding=utf-8

import PyQt4.uic
from PyQt4.QtGui import QWidget, QTabWidget, QTableWidgetItem, QMenu, QFileDialog, QApplication
from PyQt4.QtCore import *

from Share import FileShare, DirectoryShare
from downloads import Download
from TabDownloads import TabDownloads
from configuration import Configuration
from BrowserFtp import BrowserFtp
from ShareContextMenu import ShareContextMenu

from datetime import date

class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self, string, share):
        QTableWidgetItem.__init__(self, string)
        self.share = share

class TabResults(QWidget):
    resultsReceived = pyqtSignal(list)
    instance = None

    def __init__(self, search, tabs_results, tab_downloads, tabs):
        super(TabResults, self).__init__(tabs_results)
        # Vars
        self.tabs_results   = tabs_results
        self.tab_downloads  = tab_downloads
        self.tabs           = tabs
        self.blacklist      = set()
        # Load de l'UI
        PyQt4.uic.loadUi('ui/tabresult.ui', self)
        # Affichage custom
        #self.table_results.setStyleSheet(\
        #        "QTableView::item{ \
        #         border-right-style:solid; \
        #         border-width:0.5; \
        #         border-color: #9B9B9B; \
        #         }")
        self.table_results.horizontalHeader().setStretchLastSection(True)
        self.table_results.resizeColumnsToContents()
        # On autorise la creation de menu contextuel
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # Signaux
        self.customContextMenuRequested.connect(self.contextMenu)
        self.resultsReceived.connect(self.add_results)
        # On envoie la recherche
        search.do_search(self.resultsReceived.emit)
        # Instance
        TabResults.instance = self

    def _add_share(self, share):
        rows = self.table_results.rowCount()
        self.table_results.insertRow(rows)
        self.table_results.setItem(rows, 0, MyQTableWidgetItem(share.name, share))
        self.table_results.setItem(rows, 1, QTableWidgetItem(share.str_size))
        self.table_results.setItem(rows, 2, QTableWidgetItem(share.nickname))
        self.table_results.setItem(rows, 3, QTableWidgetItem("%.2f" % share.score))
        self.table_results.setItem(rows, 4, QTableWidgetItem(share.str_last_modified))
        self.table_results.setItem(rows, 5, QTableWidgetItem(share.protocol))

    def add_results(self, results):
        for share in results:
            if share.nickname in self.blacklist:
                pass
            elif share.protocol == "ftp" and (int(share.size) > 0 or type(share) == DirectoryShare):    
                self._add_share(share)

    def double_clicked(self, row, col):
        share = self.table_results.item(row, 0).share
        if type(share) is FileShare:
            self.download(share)
        else:
            browser = BrowserFtp(share.url, self.tabs, self.tabs_results, self.tab_downloads, self.tabs_results)
            self.tabs_results.addTab(browser, share.client_address)
            self.tabs_results.setCurrentWidget(browser)
            
    def download(self, share, directory=None):    
        if not directory:
            dl = Download.get_download(share, Configuration.save_dir + "/" + share.name, date.today(), 1)
        else:
            dl = Download.get_download(share, directory + "/" + share.name, date.today(), 1)
        TabDownloads.instance.add_download(dl)
        dl.start_download()
        self.tabs.setCurrentWidget(self.tab_downloads)
                
    def contextMenu(self, pos):
        menu = ShareContextMenu(self.getShare, self.getMultipleShare, self.download, self.tabs_results, self.tab_downloads, self.tabs, self, self.blacklist)
        # On affiche le menu
        menu.exec_(self.mapToGlobal(pos))
        
    def getShare(self, row=None):
        if not row:
            row = self.table_results.currentRow()
        return self.table_results.item(row, 0).share
        
    def getMultipleShare(self):
        if len(self.table_results.selectionModel().selectedRows()) > 0:
            return [self.getShare(row.row()) for row in self.table_results.selectionModel().selectedRows()]
        else:
            return self.getShare()
        
    def resizeEvent(self, event):
        maxSize = self.table_results.size().width()
        # Nom Ficher : 30%
        self.table_results.horizontalHeader().resizeSection(0, maxSize*.30)
        # Taille : 14%
        self.table_results.horizontalHeader().resizeSection(1, maxSize*.14)
        # Pseudo : 13%
        self.table_results.horizontalHeader().resizeSection(2, maxSize*.13)
        # Score : 10% 
        self.table_results.horizontalHeader().resizeSection(3, maxSize*.10)
        # Dernière modification : 18%
        self.table_results.horizontalHeader().resizeSection(4, maxSize*.18)
        event.accept()
        
class TabsResults(QTabWidget):
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        # Signaux
        QObject.connect(self, SIGNAL('tabCloseRequested(int)'), self.close_tab)
  
    def close_tab(self, index):
        self.removeTab(index)
