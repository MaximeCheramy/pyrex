#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QMainWindow, QTabWidget, QSystemTrayIcon, QIcon

import images
from TabSearch import TabSearch
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

        self.trayIcon = QSystemTrayIcon(QIcon("res/rex_18.png"), self)
        self.trayIcon.show()
        QObject.connect(self.trayIcon,
                               SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),
                               self.icon_activated)
 
        self.tabs = QTabWidget()
        QObject.connect(self.tabs, SIGNAL('currentChanged(int)'), self.change_tab)

        self.search = TabSearch(self.tabs)
        self.adv_search = TabAdvSearch(self.search, self.tabs)
        self.peers = TabPeers(self.tabs)
        self.downloads = TabDownloads(self.tabs)
        self.options = TabOptions(self.tabs)
        self.shares = TabShares(self.tabs)
        self.informations = TabInformations(self.tabs)

        self.tabs.insertTab(0, self.search, u"Recherches")
        self.tabs.insertTab(1, self.adv_search, u"Recherche avancée")
        self.tabs.insertTab(2, self.downloads, u"Téléchargements")
        self.tabs.insertTab(3, self.peers, u"Utilisateurs")
        self.tabs.insertTab(4, self.options, u'Options')
        self.tabs.insertTab(5, self.shares, u'Mes partages')
        self.tabs.insertTab(6, self.informations, u'Informations')
        
        self.setCentralWidget(self.tabs)

    def change_tab(self, tab):
        if tab == 3:
            self.peers.update_peers()
        if tab == 6:
            self.informations.update_informations()

    def closeEvent(self, event):
        #TODO: Voir le comportement souhaité lorsqu'on ferme la fenetre.
        event.accept()
 
    def icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()

