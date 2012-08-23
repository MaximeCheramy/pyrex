#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QMainWindow

import images
from search import Search
from stats import StatisticsGet
from version import VersionGet
from TabResults import TabResults, TabsResults
from TabPeers import TabPeers
from TabDownloads import TabDownloads
from TabOptions import TabOptions
from TabShares import TabShares
from TabAdvSearch import TabAdvSearch

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        PyQt4.uic.loadUi('ui/pyrex.ui', self)

        self.adv_search = TabAdvSearch(self.tabs)
        self.peers = TabPeers(self.tabs)
        self.downloads = TabDownloads(self.tabs)
        self.options = TabOptions(self.tabs)
        self.shares = TabShares(self.tabs)

        self.tabs.insertTab(1, self.adv_search, u"Recherche avancée")
        self.tabs.insertTab(2, self.downloads, u"Téléchargements")
        self.tabs.insertTab(3, self.peers, u"Utilisateurs")
        self.tabs.insertTab(4, self.options, u'Options')
        self.tabs.insertTab(5, self.shares, u'Mes partages')

        self.tabs_results = TabsResults(self.widget_recherches)
        self.widget_recherches.layout().addWidget(self.tabs_results)

    def change_tab(self, tab):
        if tab == 3:
            self.peers.update_peers()
        if tab == 6:
            self.update_informations()

    def update_informations(self):
        self.stats_get = StatisticsGet()
        self.stats_get.do_get(self.set_statistics)

        self.version_get = VersionGet()
        self.version_get.do_get(self.set_version)

    def set_statistics(self, stats):
        txt = u"Utilisateurs connectés : %d\n" % stats.users
        txt += u"Taille de vos fichiers dans la base : %s\n" % stats.shares_size_mine_str
        txt += u"Taille des fichiers dans la base : %s" % stats.shares_size_total_str
        self.statistics_label.setText(txt)

    def set_version(self, version):
        txt = "%s version %d.%d.%d\n" % \
           (version.name, version.major, version.minor, version.minor_minor)
        txt += "PyRex version 0.0.1"
        self.version_label.setText(txt)

    def search(self):
        query = str(self.search_edit1.text())
        if len(query) > 1:
            search = Search(query)
            tab_result = TabResults(search, parent=self.tabs_results)
            self.tabs_results.addTab(tab_result, query)




