# coding=utf-8

from PyQt4.QtGui import QMenu, QFileDialog, QApplication
from PyQt4.QtCore import *

from search import Search
from Share import FileShare
import BrowserFtp
import TabResults

class ShareContextMenu(QMenu):
    """ Cette classe permet la création d'un menu contextuel.
    Elle sera utilisée dans TabResults et les Browsers. """
    
    def __init__(self, getShare, getMultipleShare, download, tabs_results, tab_downloads, tabs, parent, blacklist=None):
        QMenu.__init__(self, parent)
        # Vars
        self.blacklist          = blacklist
        self.getShare           = getShare
        self.getMultipleShare   = getMultipleShare
        self.download           = download
        self.tabs_results       = tabs_results
        self.tab_downloads      = tab_downloads
        self.tabs               = tabs
        self.parent             = parent
        # Actions 
        downloadAction          = self.addAction(u"Télécharger")
        downloadToAction        = self.addAction(u"Télécharger vers...")
        copyAction              = self.addAction("Copier l'URL")
        openAction              = self.addAction("Ouvrir")
        exploreAction           = self.addAction("Parcourir le dossier")
        displaySharesAction     = self.addAction("Afficher les partages de l'utilisateur")
        noShareAction           = self.addAction("Masquer les partages de l'utilisateur")
        searchSameAction        = self.addAction("Rechercher des fichiers similaires")
        # Desactivation d'actions impossibles
        as_a_folder             = False
        for share in self.getMultipleShare():
            if type(share) is not FileShare:
                as_a_folder     = True
        if as_a_folder:
            downloadAction.setEnabled(False)
            downloadToAction.setEnabled(False)
        if isinstance(self.parent, BrowserFtp.BrowserFtp):
            noShareAction.setEnabled(False)
        #########################################################
        # On désactive les boutons qui sont pas encore implantés
        noShareAction.setEnabled(False)   
        #########################################################            
        # Signaux
        self.connect(downloadAction,      SIGNAL('triggered()'), self.download_Action)
        self.connect(downloadToAction,    SIGNAL('triggered()'), self.download_to_Action)
        self.connect(copyAction,          SIGNAL('triggered()'), self.copy_Action)
        self.connect(openAction,          SIGNAL('triggered()'), self.open_Action)
        self.connect(exploreAction,       SIGNAL('triggered()'), self.open_Action)
        self.connect(displaySharesAction, SIGNAL('triggered()'), self.display_shares_Action)
        self.connect(noShareAction,       SIGNAL('triggered()'), self.no_share_Action)
        self.connect(searchSameAction,    SIGNAL('triggered()'), self.search_same_Action)
        
    def download_Action(self):
        shares = self.getMultipleShare()
        for share in shares:
            self.download(share)
        
    def download_to_Action(self):
        directory = QFileDialog.getExistingDirectory(self)
        shares = self.getMultipleShare()
        for share in shares:
            self.download(share, directory)
        
    def copy_Action(self):
        pressPaper = QApplication.clipboard()
        shares = self.getMultipleShare()
        if len(shares) == 1:
            pressPaper.setText(shares.url)
        else:
            text = ""
            for share in shares:
                text += share.url + "\n"
            pressPaper.setText(text)
        
    def open_Action(self):
        share = self.getShare()
        browser = BrowserFtp.BrowserFtp(share.url, self.tabs, self.tabs_results, self.tab_downloads, self.tabs_results)
        self.tabs_results.addTab(browser, share.client_address)
        self.tabs_results.setCurrentWidget(browser)
        
    def no_share_Action(self):
        share = self.getShare()
        if blacklist:
            self.blacklist.add(share.nickname)
        
    def display_shares_Action(self):
        share = self.getShare()
        browser = BrowserFtp.BrowserFtp("ftp://"+str(share.client_address)+":"+str(share.port), self.tabs, self.tabs_results, self.tab_downloads, self.tabs_results)
        self.tabs_results.addTab(browser, share.client_address)
        self.tabs_results.setCurrentWidget(browser)
        
    def search_same_Action(self):
        share = self.getShare()
        search = Search(share.name)
        tab_result = TabResults.TabResults(search, self.tabs_results, self.tab_downloads, self.tabs)
        self.tabs_results.addTab(tab_result, search.query)
        self.tabs_results.setCurrentWidget(tab_result)
