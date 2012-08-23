#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QMainWindow

import images
from search import Search
from TabResults import TabResults, TabsResults
from TabPeers import TabPeers
from TabDownloads import TabDownloads
from TabOptions import TabOptions
from TabShares import TabShares
from TabAdvSearch import TabAdvSearch
from TabInformations import TabInformations

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        PyQt4.uic.loadUi('ui/pyrex.ui', self)

        self.adv_search = TabAdvSearch(self.tabs)
        self.peers = TabPeers(self.tabs)
        self.downloads = TabDownloads(self.tabs)
        self.options = TabOptions(self.tabs)
        self.shares = TabShares(self.tabs)
        self.informations = TabInformations(self.tabs)

        self.tabs.insertTab(1, self.adv_search, u"Recherche avancée")
        self.tabs.insertTab(2, self.downloads, u"Téléchargements")
        self.tabs.insertTab(3, self.peers, u"Utilisateurs")
        self.tabs.insertTab(4, self.options, u'Options')
        self.tabs.insertTab(5, self.shares, u'Mes partages')
        self.tabs.insertTab(6, self.informations, u'Informations')

        self.tabs_results = TabsResults(self.widget_recherches)
        self.widget_recherches.layout().addWidget(self.tabs_results)

    def change_tab(self, tab):
        if tab == 3:
            self.peers.update_peers()
        if tab == 6:
            self.informations.update_informations()

    def search(self):
        query = str(self.search_edit1.text())
        if len(query) > 1:
            search = Search(query)
            tab_result = TabResults(search, parent=self.tabs_results)
            self.tabs_results.addTab(tab_result, query)

