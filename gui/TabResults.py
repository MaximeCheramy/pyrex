# coding=utf-8

import PyQt4.uic
from PyQt4.QtGui import QWidget, QTabWidget, QTableWidgetItem, QMenu, QFileDialog, QApplication
from PyQt4.QtCore import *

from Share import FileShare, DirectoryShare
from downloads import Download
from TabDownloads import TabDownloads
from configuration import Configuration
from BrowserFtp import BrowserFtp
from search import Search

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
        self.tabs_results = tabs_results
        self.tab_downloads = tab_downloads
        self.tabs = tabs
        self.blacklist = set()
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
            elif share.protocol == "ftp" and share.nickname != "" and (int(share.size) > 0 or type(share) == DirectoryShare):    
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
            dl = Download.get_download(share, Configuration.save_dir + "/" + share.name, date.today(), 1)
        else:
            dl = Download.get_download(share, directory + "/" + share.name, date.today(), 1)
        TabDownloads.instance.add_download(dl)
        dl.start_download()
        self.tabs.setCurrentWidget(self.tab_downloads)
      
    def contextMenu(self, pos):
        menu = QMenu()
        # Actions 
        downloadAction      = menu.addAction(u"Télécharger")
        downloadToAction    = menu.addAction(u"Télécharger vers...")
        copyAction          = menu.addAction("Copier l'URL")
        openAction          = menu.addAction("Ouvrir")
        exploreAction       = menu.addAction("Parcourir le dossier")
        displaySharesAction = menu.addAction("Afficher les partages de l'utilisateur")
        noShareAction       = menu.addAction("Masquer les partages de l'utilisateur")
        searchSameAction    = menu.addAction("Rechercher des fichiers similaires")
        # Desactivation d'actions impossibles
        if type(self.getShare()) is not FileShare:
            downloadAction.setEnabled(False)
            downloadToAction.setEnabled(False)
        #########################################################
        # On désactive les boutons qui sont pas encore implantés
        noShareAction.setEnabled(False)   
        #########################################################            
        # Signaux
        self.connect(downloadAction, SIGNAL('triggered()'), self.download_Action)
        self.connect(downloadToAction, SIGNAL('triggered()'), self.download_to_Action)
        self.connect(copyAction, SIGNAL('triggered()'), self.copy_Action)
        self.connect(openAction, SIGNAL('triggered()'), self.open_Action)
        self.connect(exploreAction, SIGNAL('triggered()'), self.open_Action)
        self.connect(displaySharesAction, SIGNAL('triggered()'), self.display_shares_Action)
        self.connect(noShareAction, SIGNAL('triggered()'), self.no_share_Action)
        self.connect(searchSameAction, SIGNAL('triggered()'), self.search_same_Action)
        # On affiche le menu
        menu.exec_(self.mapToGlobal(pos))

    def getShare(self):
        row = self.table_results.currentRow()
        return self.table_results.item(row, 0).share
        
    def getMultipleShare(self):
        if len(self.table_results.selectionModel().selectedRows()) > 0:
            return [self.table_results.item(row.row(), 0).share for row in self.table_results.selectionModel().selectedRows()]
        else:
            return self.getShare()
        
    def download_Action(self):
        shares = self.getMultipleShare()
        for share in shares:
            self.download(share)
        
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
        
    def no_share_Action(self):
        share = self.getShare()
        self.blacklist.add(share.nickname)
        
    def display_shares_Action(self):
        share = self.getShare()
        browser = BrowserFtp("ftp://"+str(share.client_address)+":"+str(share.port), self.tabs_results)
        self.tabs_results.addTab(browser, share.client_address)
        self.tabs_results.setCurrentWidget(browser)
        
    def search_same_Action(self):
        share = self.getShare()
        search = Search(share.name)
        tab_result = TabResults(search, self.tabs_results, self.tab_downloads, self.tabs)
        self.tabs_results.addTab(tab_result, search.query)
        self.tabs_results.setCurrentWidget(tab_result)
        
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
        QObject.connect(self, SIGNAL('tabCloseRequested(int)'), self.close_tab)
        
    def close_tab(self, index):
        self.removeTab(index)
