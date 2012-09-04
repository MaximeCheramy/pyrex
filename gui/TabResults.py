# coding=utf-8

import PyQt4.uic
from PyQt4.QtGui import QWidget, QTabWidget, QTableWidgetItem, QMenu, QFileDialog, QApplication
from PyQt4.QtCore import *

from Share import FileShare
from downloads import Download
from TabDownloads import TabDownloads
from configuration import Configuration
from BrowserFtp import BrowserFtp

from datetime import date

class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self, string, share):
        QTableWidgetItem.__init__(self, string)
        self.share = share


class TabResults(QWidget):
    resultsReceived = pyqtSignal(list)

    def __init__(self, search, tabs_results):
        super(TabResults, self).__init__(tabs_results)
        self.tabs_results = tabs_results
        self.pos = None
        # Load de l'UI
        PyQt4.uic.loadUi('ui/tabresult.ui', self)
        # On autorise la creation de menu contextuel
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # Signaux
        self.customContextMenuRequested.connect(self.contextMenu)
        self.resultsReceived.connect(self.add_results)
        # On envoie la recherche
        search.do_search(self.resultsReceived.emit)

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
            self._add_share(share)

    def double_clicked(self, row, col):
        share = self.table_results.item(row, 0).share
        if type(share) is FileShare:
            self.download(share)
        else:
            browser = BrowserFtp(share.url, self.tabs_results)
            self.tabs_results.addTab(browser, share.client_address)
            self.tabs_results.setCurrentWidget(browser)


    def download(self, share, directory=None):
        if not directory:
            dl = Download.get_download(share, Configuration.save_dir + "/" + share.name, date.today())
        else:
            dl = Download.get_download(share, directory + "/" + share.name, date.today())
        TabDownloads.instance.add_download(dl)
        dl.start_download()
      
    def contextMenu(self, pos):
        self.pos = pos
        menu = QMenu()
        # Actions 
        downloadAction      = menu.addAction(u"Télécharger")
        downloadToAction    = menu.addAction(u"Télécharger vers...")
        copyAction          = menu.addAction("Copier l'URL")
        openAction          = menu.addAction("Ouvrir")
        exploreAction       = menu.addAction("Parcourir le dossier")
        shareAction         = menu.addAction("Afficher les partages de l'utilisateur")
        noShareAction       = menu.addAction("Masquer les partages de l'utilisateur")
        searchSameAction    = menu.addAction("Rechercher des fichiers similaires")
        # Signaux
        self.connect(downloadAction, SIGNAL('triggered()'), self.download_Action)
        self.connect(downloadToAction, SIGNAL('triggered()'), self.download_to_Action)
        self.connect(copyAction, SIGNAL('triggered()'), self.copy_Action)
        self.connect(openAction, SIGNAL('triggered()'), self.open_Action)
        self.connect(exploreAction, SIGNAL('triggered()'), self.open_Action)
        #self.connect(shareAction, SIGNAL('triggered()'), self.)
        #self.connect(noShareAction, SIGNAL('triggered()'), self.)
        #self.connect(searchSameAction, SIGNAL('triggered()'), self.)
        menu.exec_(self.mapToGlobal(pos))

    def getShare(self):
        row = self.table_results.itemAt(self.pos).row()
        return self.table_results.item(row-2, 0).share
        
    def download_Action(self):
        self.download(self.getShare())
        
    def download_to_Action(self):
        directory = QFileDialog.getExistingDirectory(self)
        self.download(self.getShare(), directory)
        
    def copy_Action(self):
        pressPaper = QApplication.clipboard()
        pressPaper.setText(self.getShare().url)
        
    def open_Action(self):
        share = self.getShare()
        browser = BrowserFtp(share.url, self.tabs_results)
        self.tabs_results.addTab(browser, share.client_address)
        self.tabs_results.setCurrentWidget(browser)
        
class TabsResults(QTabWidget):
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        QObject.connect(self, SIGNAL('tabCloseRequested(int)'), self.close_tab)
        
    def close_tab(self, index):
        self.removeTab(index)
