#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget

from search import Search
from TabResults import TabResults, TabsResults

class TabSearch(QWidget):
    instance = None

    def __init__(self, search, tab_downloads, parent):
        QWidget.__init__(self, parent)
        TabSearch.instance = self
        self.tab_downloads = tab_downloads
        self.tabs = parent
        # Load de l'UI
        PyQt4.uic.loadUi('ui/search.ui', self)
        # Init
        self.tabs_results = TabsResults(self.widget_searches)
        self.widget_searches.layout().addWidget(self.tabs_results)
        
    def search(self):
        query = unicode(self.search_edit.text().toUtf8(), 'utf-8')
        if len(query) > 1:
            self.add_search(Search(query))

    def add_search(self, search):
        tab_result = TabResults(search, self.tabs_results, self.tab_downloads, self.tabs)
        self.tabs_results.addTab(tab_result, search.query)
        self.tabs_results.setCurrentWidget(tab_result)
        # On connecte les icones copier et télécharger sélection
        # TODO
        #self.btn_copy_url.clicked.connect(.copy_Action)
        #self.btn_download.clicked.connect(.menu.download_Action)
